"""ANOVA suitability check and decision guardrail utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from scipy import stats
except ImportError:  # pragma: no cover - fallback is for partially installed environments.
    stats = None

from .data_validation import participant_id_issue, repeated_or_nested_hint_columns
from .utils import load_yaml, project_path, write_text


STATUS_ORDER = {"pass": 0, "warning": 1, "diagnostic_only": 2, "stop_analysis": 3}
DECISION_ORDER = {
    "classical_anova_recommended": 0,
    "welch_anova_recommended": 1,
    "diagnostic_only": 2,
    "stop_analysis": 3,
}


@dataclass
class CheckResult:
    name: str
    status: str
    message: str
    values: dict[str, Any] = field(default_factory=dict)


@dataclass
class OutcomeDecision:
    outcome: str
    decision: str
    recommended_analysis: str | None
    recommended_posthoc: str | None
    checks: list[CheckResult]


def _threshold(rules: dict[str, Any], section: str, key: str, default: Any) -> Any:
    return rules.get("thresholds", {}).get(section, {}).get(key, default)


def _format_p(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "NA"
    if value < 0.001:
        return "< .001"
    return f"{value:.3f}".replace("0.", ".")


def _max_status(results: list[CheckResult]) -> str:
    return max((result.status for result in results), key=lambda item: STATUS_ORDER[item])


def _overall_decision(outcomes: list[OutcomeDecision], structural_checks: list[CheckResult]) -> str:
    if any(check.status == "stop_analysis" for check in structural_checks):
        return "stop_analysis"
    return max((outcome.decision for outcome in outcomes), key=lambda item: DECISION_ORDER[item])


def _analysis_labels(decision: str) -> tuple[str | None, str | None]:
    if decision == "classical_anova_recommended":
        return "classical_one_way_anova", "tukey_hsd"
    if decision == "welch_anova_recommended":
        return "welch_anova", "games_howell"
    return None, None


def load_inputs(
    analysis_plan_path: str | Path = "config/analysis_plan.yaml",
    rules_path: str | Path = "config/statistical_decision_rules.yaml",
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any]]:
    plan = load_yaml(analysis_plan_path)
    rules = load_yaml(rules_path)
    dataset_path = project_path(plan["dataset_path"])
    return pd.read_csv(dataset_path), plan, rules


def structural_checks(df: pd.DataFrame, plan: dict[str, Any], rules: dict[str, Any]) -> list[CheckResult]:
    analysis = plan.get("analysis", {})
    grouping = analysis.get("grouping_variable")
    outcomes = analysis.get("outcome_variables", [])
    checks: list[CheckResult] = []

    if analysis.get("analysis_type") != rules.get("scope", {}).get("supported_analysis_type"):
        checks.append(CheckResult("analysis_type", "stop_analysis", "Only between-subjects one-way ANOVA is supported in this MVP."))
    else:
        checks.append(CheckResult("analysis_type", "pass", "Analysis type is supported.", {"analysis_type": analysis.get("analysis_type")}))

    if grouping not in df.columns:
        checks.append(CheckResult("grouping_variable_present", "stop_analysis", "Grouping variable is missing.", {"grouping_variable": grouping}))
        return checks
    checks.append(CheckResult("grouping_variable_present", "pass", "Grouping variable is present.", {"grouping_variable": grouping}))

    group_counts = df[grouping].dropna().value_counts().to_dict()
    valid_group_count = len(group_counts)
    if valid_group_count < 2:
        checks.append(CheckResult("minimum_group_count", "stop_analysis", "Fewer than two valid groups were found.", {"valid_group_count": valid_group_count}))
    else:
        checks.append(CheckResult("minimum_group_count", "pass", "At least two valid groups were found.", {"valid_group_count": valid_group_count, "group_counts": group_counts}))

    expected_groups = rules.get("scope", {}).get("expected_groups", [])
    unexpected = sorted(set(group_counts) - set(expected_groups))
    missing_expected = sorted(set(expected_groups) - set(group_counts))
    if unexpected or missing_expected:
        checks.append(CheckResult(
            "expected_demo_groups",
            "warning",
            "Group labels differ from the recommended demo groups.",
            {"expected_groups": expected_groups, "unexpected_groups": unexpected, "missing_expected_groups": missing_expected},
        ))
    else:
        checks.append(CheckResult("expected_demo_groups", "pass", "All recommended demo groups are present.", {"expected_groups": expected_groups}))

    missing_outcomes = [outcome for outcome in outcomes if outcome not in df.columns]
    if missing_outcomes:
        checks.append(CheckResult("dependent_variables_present", "stop_analysis", "One or more dependent variables are missing.", {"missing": missing_outcomes}))
    else:
        checks.append(CheckResult("dependent_variables_present", "pass", "All dependent variables are present.", {"outcomes": outcomes}))

    nonnumeric = [outcome for outcome in outcomes if outcome in df.columns and not pd.api.types.is_numeric_dtype(df[outcome])]
    if nonnumeric:
        checks.append(CheckResult("dependent_variables_numeric", "stop_analysis", "One or more dependent variables are nonnumeric.", {"nonnumeric": nonnumeric}))
    else:
        checks.append(CheckResult("dependent_variables_numeric", "pass", "All dependent variables are numeric.", {"outcomes": outcomes}))

    participant_issue = participant_id_issue(df, grouping)
    if participant_issue == "duplicated_participant_id_across_groups":
        checks.append(CheckResult("participant_id_unique", "stop_analysis", "The same participant_id appears in multiple groups.", {"issue": participant_issue}))
    elif participant_issue == "duplicated_participant_id_records":
        checks.append(CheckResult("participant_id_unique", "stop_analysis", "Duplicate participant_id records suggest repeated observations.", {"issue": participant_issue}))
    else:
        checks.append(CheckResult("participant_id_unique", "pass", "participant_id is unique when present."))

    nested_hints = repeated_or_nested_hint_columns(df)
    if nested_hints:
        checks.append(CheckResult("repeated_or_nested_structure", "stop_analysis", "Columns suggest repeated-measures or nested/clustered data, which is outside this MVP.", {"hint_columns": nested_hints}))
    else:
        checks.append(CheckResult("repeated_or_nested_structure", "pass", "No repeated-measures or nested/cluster hint columns detected."))

    return checks


def missingness_check(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any]) -> CheckResult:
    pass_max = _threshold(rules, "missingness", "pass_max_rate", 0.05)
    warning_max = _threshold(rules, "missingness", "warning_max_rate", 0.20)
    group_diagnostic = _threshold(rules, "missingness", "group_diagnostic_rate", 0.30)

    key_vars = [grouping, outcome]
    variable_rates = {var: float(df[var].isna().mean()) for var in key_vars}
    group_rates = df.groupby(grouping, dropna=False)[outcome].apply(lambda item: float(item.isna().mean())).to_dict()
    max_variable_rate = max(variable_rates.values())
    max_group_rate = max(group_rates.values()) if group_rates else 1.0

    if max_variable_rate > warning_max or max_group_rate > group_diagnostic:
        status = "diagnostic_only"
        message = "Missingness is too high for automatic formal reporting."
    elif max_variable_rate > pass_max:
        status = "warning"
        message = "Missingness is present and should be reviewed; no automatic imputation is applied."
    else:
        status = "pass"
        message = "Missingness is within the pass threshold; no automatic imputation is applied."
    return CheckResult("missingness", status, message, {"variable_missing_rates": variable_rates, "group_missing_rates": group_rates})


def sample_size_check(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any]) -> CheckResult:
    pass_min = _threshold(rules, "group_sample_size", "pass_min_n", 20)
    warning_min = _threshold(rules, "group_sample_size", "warning_min_n", 10)
    stop_below = _threshold(rules, "group_sample_size", "stop_below_n", 5)
    counts = df.dropna(subset=[grouping, outcome]).groupby(grouping)[outcome].count().to_dict()
    min_n = min(counts.values()) if counts else 0

    if min_n < stop_below:
        status = "stop_analysis"
        message = "At least one group has fewer than 5 valid cases or is empty."
    elif min_n < warning_min:
        status = "diagnostic_only"
        message = "At least one group has fewer than 10 valid cases."
    elif min_n < pass_min:
        status = "warning"
        message = "At least one group has 10-19 valid cases."
    else:
        status = "pass"
        message = "Every group has at least 20 valid cases."
    return CheckResult("group_sample_size", status, message, {"valid_n_by_group": counts, "min_group_n": min_n})


def sample_balance_check(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any]) -> CheckResult:
    pass_ratio = _threshold(rules, "sample_size_balance", "pass_max_ratio", 2)
    warning_ratio = _threshold(rules, "sample_size_balance", "warning_max_ratio", 4)
    counts = df.dropna(subset=[grouping, outcome]).groupby(grouping)[outcome].count()
    min_n = int(counts.min()) if not counts.empty else 0
    max_n = int(counts.max()) if not counts.empty else 0
    ratio = float(max_n / min_n) if min_n else float("inf")

    if ratio > warning_ratio:
        status = "diagnostic_only"
        message = "Group sample sizes are severely imbalanced."
    elif ratio > pass_ratio:
        status = "warning"
        message = "Group sample sizes are moderately imbalanced."
    else:
        status = "pass"
        message = "Group sample sizes are acceptably balanced."
    return CheckResult("sample_size_balance", status, message, {"max_n": max_n, "min_n": min_n, "max_to_min_ratio": round(ratio, 3)})


def outlier_check(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any]) -> CheckResult:
    multiplier = _threshold(rules, "outliers", "iqr_multiplier", 1.5)
    pass_max = _threshold(rules, "outliers", "pass_max_rate", 0.02)
    warning_max = _threshold(rules, "outliers", "warning_max_rate", 0.05)
    concentration_rate = _threshold(rules, "outliers", "concentrated_group_rate", 0.10)
    concentration_share = _threshold(rules, "outliers", "concentrated_share_of_all_outliers", 0.60)

    working = df.dropna(subset=[grouping, outcome]).copy()
    working["_outlier"] = False
    group_details: dict[str, dict[str, Any]] = {}
    for group, group_df in working.groupby(grouping):
        q1 = group_df[outcome].quantile(0.25)
        q3 = group_df[outcome].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        mask = (working[grouping] == group) & ((working[outcome] < lower) | (working[outcome] > upper))
        working.loc[mask, "_outlier"] = True
        group_n = int((working[grouping] == group).sum())
        outlier_n = int(mask.sum())
        group_details[str(group)] = {
            "n": group_n,
            "outliers": outlier_n,
            "outlier_rate": round(outlier_n / group_n, 4) if group_n else None,
            "lower_fence": round(float(lower), 3),
            "upper_fence": round(float(upper), 3),
        }

    total_n = len(working)
    total_outliers = int(working["_outlier"].sum())
    rate = total_outliers / total_n if total_n else 1.0
    max_group_rate = max((details["outlier_rate"] or 0 for details in group_details.values()), default=0)
    max_group_share = max((details["outliers"] / total_outliers for details in group_details.values()), default=0) if total_outliers else 0
    concentrated = total_outliers > 0 and max_group_rate > concentration_rate and max_group_share >= concentration_share

    if rate > warning_max or concentrated:
        status = "diagnostic_only"
        message = "Outlier pattern requires diagnostic-only handling and human review."
    elif rate > pass_max:
        status = "warning"
        message = "Outliers are present and should be reviewed; no automatic deletion is applied."
    else:
        status = "pass"
        message = "Outlier rate is within the pass threshold; no automatic deletion is applied."
    return CheckResult("outliers_iqr", status, message, {"overall_outlier_rate": round(rate, 4), "total_outliers": total_outliers, "by_group": group_details})


def normality_check(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any], outlier_status: str) -> CheckResult:
    alpha = _threshold(rules, "normality", "alpha", 0.05)
    warning_skew = _threshold(rules, "normality", "warning_skew_abs", 1)
    warning_kurtosis = _threshold(rules, "normality", "warning_kurtosis_abs", 3)
    severe_skew = _threshold(rules, "normality", "severe_skew_abs", 2)
    severe_kurtosis = _threshold(rules, "normality", "severe_kurtosis_abs", 7)
    small_sample_n = _threshold(rules, "normality", "small_sample_n", 20)

    details: dict[str, dict[str, Any]] = {}
    has_warning = False
    has_severe_small_sample_problem = False
    for group, group_df in df.dropna(subset=[grouping, outcome]).groupby(grouping):
        values = group_df[outcome].astype(float)
        n = int(values.count())
        shapiro_w = None
        shapiro_p = None
        if stats is not None and 3 <= n <= 5000:
            shapiro = stats.shapiro(values)
            shapiro_w = float(shapiro.statistic)
            shapiro_p = float(shapiro.pvalue)

        skew = float(values.skew()) if n >= 3 else None
        kurtosis = float(values.kurt()) if n >= 4 else None
        severe_shape = (
            (skew is not None and abs(skew) > severe_skew)
            or (kurtosis is not None and abs(kurtosis) > severe_kurtosis)
        )
        warning_shape = (
            (skew is not None and abs(skew) > warning_skew)
            or (kurtosis is not None and abs(kurtosis) > warning_kurtosis)
            or (shapiro_p is not None and shapiro_p < alpha)
        )
        if warning_shape:
            has_warning = True
        if n < small_sample_n and severe_shape:
            has_severe_small_sample_problem = True

        details[str(group)] = {
            "n": n,
            "shapiro_w": None if shapiro_w is None else round(shapiro_w, 4),
            "shapiro_p": None if shapiro_p is None else round(shapiro_p, 4),
            "skewness": None if skew is None else round(skew, 3),
            "kurtosis": None if kurtosis is None else round(kurtosis, 3),
        }

    if has_severe_small_sample_problem or (outlier_status == "diagnostic_only" and has_warning):
        status = "diagnostic_only"
        message = "Normality risk is high enough that the workflow should not auto-generate formal conclusions."
    elif has_warning:
        status = "warning"
        message = "At least one group shows a normality warning; Shapiro-Wilk p < .05 is not treated as automatic failure."
    else:
        status = "pass"
        message = "No severe group-level normality issue detected."
    if stats is None:
        message += " scipy is unavailable, so Shapiro-Wilk p-values were not computed."
    return CheckResult("normality", status, message, {"by_group": details})


def variance_homogeneity_check(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any]) -> CheckResult:
    alpha = _threshold(rules, "variance_homogeneity", "alpha", 0.05)
    acceptable_ratio = _threshold(rules, "variance_homogeneity", "acceptable_max_variance_ratio", 2)
    strong_alpha = _threshold(rules, "variance_homogeneity", "strong_warning_alpha", 0.01)
    strong_ratio = _threshold(rules, "variance_homogeneity", "strong_warning_variance_ratio", 4)
    grouped = [group[outcome].astype(float).to_numpy() for _, group in df.dropna(subset=[grouping, outcome]).groupby(grouping)]
    variances = df.dropna(subset=[grouping, outcome]).groupby(grouping)[outcome].var().to_dict()
    positive_variances = [value for value in variances.values() if value and value > 0]
    variance_ratio = max(positive_variances) / min(positive_variances) if positive_variances else float("inf")

    levene_stat = None
    levene_p = None
    if stats is not None and len(grouped) >= 2 and all(len(group) >= 2 for group in grouped):
        levene = stats.levene(*grouped, center="median")
        levene_stat = float(levene.statistic)
        levene_p = float(levene.pvalue)

    variance_violation = (levene_p is not None and levene_p < alpha) or variance_ratio > acceptable_ratio
    strong_warning = (levene_p is not None and levene_p < strong_alpha) and variance_ratio > strong_ratio
    if strong_warning:
        status = "warning"
        message = "Strong variance heterogeneity warning; Welch ANOVA is recommended unless additional risks require diagnostic-only handling."
    elif variance_violation:
        status = "warning"
        message = "Variance homogeneity is not met or is uncertain; Welch ANOVA is recommended."
    else:
        status = "pass"
        message = "Variance homogeneity is acceptable; classical ANOVA is eligible."
    if stats is None:
        message += " scipy is unavailable, so Levene's test p-value was not computed."
    return CheckResult("variance_homogeneity", status, message, {
        "levene_statistic": None if levene_stat is None else round(levene_stat, 4),
        "levene_p": None if levene_p is None else round(levene_p, 4),
        "variance_by_group": {str(group): round(float(value), 4) for group, value in variances.items()},
        "max_min_variance_ratio": round(float(variance_ratio), 3),
        "variance_violation": variance_violation,
        "strong_warning": strong_warning,
    })


def evaluate_outcome(df: pd.DataFrame, grouping: str, outcome: str, rules: dict[str, Any]) -> OutcomeDecision:
    checks = [
        missingness_check(df, grouping, outcome, rules),
        sample_size_check(df, grouping, outcome, rules),
        sample_balance_check(df, grouping, outcome, rules),
    ]
    outliers = outlier_check(df, grouping, outcome, rules)
    checks.append(outliers)
    checks.append(normality_check(df, grouping, outcome, rules, outliers.status))
    variance = variance_homogeneity_check(df, grouping, outcome, rules)
    checks.append(variance)

    if any(check.status == "stop_analysis" for check in checks):
        decision = "stop_analysis"
    elif any(check.status == "diagnostic_only" for check in checks):
        decision = "diagnostic_only"
    elif variance.values.get("strong_warning") and any(check.name in {"group_sample_size", "sample_size_balance", "outliers_iqr"} and check.status == "warning" for check in checks):
        decision = "diagnostic_only"
    elif variance.values.get("variance_violation"):
        decision = "welch_anova_recommended"
    else:
        decision = "classical_anova_recommended"

    analysis, posthoc = _analysis_labels(decision)
    return OutcomeDecision(outcome, decision, analysis, posthoc, checks)


def run_suitability_check(
    analysis_plan_path: str | Path = "config/analysis_plan.yaml",
    rules_path: str | Path = "config/statistical_decision_rules.yaml",
    output_dir: str | Path = "outputs",
) -> dict[str, Any]:
    df, plan, rules = load_inputs(analysis_plan_path, rules_path)
    grouping = plan["analysis"]["grouping_variable"]
    outcomes = plan["analysis"]["outcome_variables"]
    structural = structural_checks(df, plan, rules)

    if any(check.status == "stop_analysis" for check in structural):
        outcome_decisions: list[OutcomeDecision] = []
    else:
        outcome_decisions = [evaluate_outcome(df, grouping, outcome, rules) for outcome in outcomes]

    overall = _overall_decision(outcome_decisions, structural) if outcome_decisions else "stop_analysis"
    report = render_suitability_report(df, plan, structural, outcome_decisions, overall)
    review_prompt = render_human_review_required(plan, outcome_decisions, overall)
    suitability_path = write_text(Path(output_dir) / "anova_suitability_check.md", report)
    review_path = write_text(Path(output_dir) / "human_review_required.md", review_prompt)
    return {
        "overall_decision": overall,
        "outcomes": outcome_decisions,
        "suitability_report": suitability_path,
        "human_review_required": review_path,
    }


def render_suitability_report(
    df: pd.DataFrame,
    plan: dict[str, Any],
    structural: list[CheckResult],
    outcomes: list[OutcomeDecision],
    overall: str,
) -> str:
    lines = [
        "# ANOVA Suitability Check",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "This diagnostic report is a statistical decision guardrail. It recommends an analysis path but does not authorize formal statistical reporting before human review.",
        "",
        "## Overall Recommendation",
        "",
        f"- Overall decision: `{overall}`",
        f"- Dataset rows: {len(df)}",
        f"- Grouping variable: `{plan['analysis']['grouping_variable']}`",
        f"- Outcome variables: {', '.join(f'`{outcome}`' for outcome in plan['analysis']['outcome_variables'])}",
        "",
        "## Structural Checks",
        "",
        "| Check | Status | Key values | Interpretation |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(_render_check_rows(structural))

    for outcome in outcomes:
        lines.extend([
            "",
            f"## Outcome: `{outcome.outcome}`",
            "",
            f"- Decision: `{outcome.decision}`",
            f"- Recommended analysis after approval: `{outcome.recommended_analysis or 'none'}`",
            f"- Recommended post hoc after approval: `{outcome.recommended_posthoc or 'none'}`",
            "",
            "| Check | Status | Key values | Interpretation |",
            "| --- | --- | --- | --- |",
        ])
        lines.extend(_render_check_rows(outcome.checks))

    lines.extend([
        "",
        "## Guardrail Notes",
        "",
        "- No missing values are automatically imputed.",
        "- IQR outliers are flagged only; they are not automatically deleted.",
        "- Shapiro-Wilk p < .05 is treated as a warning, not an automatic failure.",
        "- Ordinary/classical ANOVA is used only when variance homogeneity is acceptable.",
        "- When variance homogeneity is not met or is uncertain, the recommended path switches to Welch ANOVA with Games-Howell post hoc tests.",
        "- Formal APA results, formal tables, figures, and Word reports must wait until human approval is recorded.",
    ])
    return "\n".join(lines) + "\n"


def render_human_review_required(plan: dict[str, Any], outcomes: list[OutcomeDecision], overall: str) -> str:
    lines = [
        "# Human Review Required",
        "",
        "The suitability check has finished. The workflow is intentionally paused before formal statistical reporting.",
        "",
        f"- Overall recommendation: `{overall}`",
        f"- Approval file required: `{plan['human_review']['decision_file']}`",
        "",
        "## Outcome-Level Recommendations",
        "",
        "| Outcome | Decision | Analysis path | Post hoc |",
        "| --- | --- | --- | --- |",
    ]
    if outcomes:
        for outcome in outcomes:
            lines.append(f"| `{outcome.outcome}` | `{outcome.decision}` | `{outcome.recommended_analysis or 'none'}` | `{outcome.recommended_posthoc or 'none'}` |")
    else:
        lines.append("| none | `stop_analysis` | none | none |")

    lines.extend([
        "",
        "## Required Human Action",
        "",
        "Review `outputs/anova_suitability_check.md`. If the recommended path is appropriate, create `config/human_review_decision.yaml` from `config/human_review_decision.example.yaml` and set:",
        "",
        "```yaml",
        "approval_status: approved",
        "approved_analysis_path: classical_anova",
        "```",
        "",
        "Use `approved_analysis_path: welch_anova` if the reviewed recommendation is Welch ANOVA.",
        "",
        "If the decision is `diagnostic_only` or `stop_analysis`, do not approve formal report generation without revising the data, analysis plan, or MVP scope.",
        "",
        "Until approval is present, the workflow must not generate APA result paragraphs, formal statistical tables, result figures, or Word reports.",
    ])
    return "\n".join(lines) + "\n"


def _render_check_rows(checks: list[CheckResult]) -> list[str]:
    return [
        f"| `{check.name}` | `{check.status}` | {_compact_values(check.values)} | {check.message} |"
        for check in checks
    ]


def _compact_values(values: dict[str, Any]) -> str:
    if not values:
        return "-"
    parts = []
    for key, value in values.items():
        if isinstance(value, float):
            display = _format_p(value) if key.endswith("_p") else f"{value:.3f}"
        else:
            display = str(value)
        display = display.replace("|", "/")
        parts.append(f"{key}: {display}")
    return "<br>".join(parts)
