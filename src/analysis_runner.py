"""Pure Python analysis runner for classical ANOVA, Welch ANOVA, and post hoc tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pingouin as pg
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from .utils import load_yaml, project_path


def run_confirmed_analyses(
    analysis_plan_path: str | Path = "config/analysis_plan.yaml",
    decision_path: str | Path = "config/human_review_decision.yaml",
) -> dict[str, Any]:
    plan = load_yaml(analysis_plan_path)
    decision = load_yaml(decision_path)
    _validate_human_approval(plan, decision)

    data = pd.read_csv(project_path(plan["dataset_path"]))
    grouping = plan["analysis"]["grouping_variable"]
    group_order = plan["analysis"].get("condition_order") or list(data[grouping].dropna().unique())
    outcomes = plan["analysis"]["outcome_variables"]
    alpha = plan["reporting"].get("alpha", 0.05)

    results: dict[str, Any] = {
        "grouping_variable": grouping,
        "group_order": group_order,
        "outcomes": {},
        "alpha": alpha,
    }
    for outcome in outcomes:
        approved = decision["outcome_decisions"][outcome]
        analysis_path = approved["approved_analysis_path"]
        if analysis_path == "classical_anova":
            outcome_result = _classical_anova(data, grouping, outcome, group_order, alpha)
        elif analysis_path == "welch_anova":
            outcome_result = _welch_anova(data, grouping, outcome, group_order, alpha)
        else:
            raise ValueError(f"Unsupported approved analysis path for {outcome}: {analysis_path}")
        outcome_result["approved_analysis_path"] = analysis_path
        outcome_result["approved_posthoc_method"] = approved.get("approved_posthoc_method")
        results["outcomes"][outcome] = outcome_result
    return results


def _validate_human_approval(plan: dict[str, Any], decision: dict[str, Any]) -> None:
    if decision.get("approval_status") != "approved":
        raise RuntimeError("Formal analysis is blocked until approval_status is approved.")
    outcome_decisions = decision.get("outcome_decisions", {})
    missing = [outcome for outcome in plan["analysis"]["outcome_variables"] if outcome not in outcome_decisions]
    if missing:
        raise RuntimeError(f"Missing outcome-level human approval for: {', '.join(missing)}")
    not_approved = [
        outcome for outcome, item in outcome_decisions.items()
        if item.get("approval_status") != "approved"
    ]
    if not_approved:
        raise RuntimeError(f"Outcome-level approval is not approved for: {', '.join(not_approved)}")


def _descriptives(data: pd.DataFrame, grouping: str, outcome: str, group_order: list[str]) -> dict[str, Any]:
    desc = {}
    for group in group_order:
        values = data.loc[data[grouping] == group, outcome].dropna()
        desc[group] = {
            "n": int(values.count()),
            "mean": float(values.mean()),
            "sd": float(values.std(ddof=1)),
        }
    return desc


def _classical_anova(data: pd.DataFrame, grouping: str, outcome: str, group_order: list[str], alpha: float) -> dict[str, Any]:
    working = data[[grouping, outcome]].dropna().copy()
    working[grouping] = pd.Categorical(working[grouping], categories=group_order, ordered=True)
    formula = f"{outcome} ~ C({grouping})"
    model = smf.ols(formula, data=working).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    effect_row = anova_table.loc[f"C({grouping})"]
    residual_row = anova_table.loc["Residual"]
    ss_effect = float(effect_row["sum_sq"])
    ss_total = float(anova_table["sum_sq"].sum())
    eta_sq = ss_effect / ss_total if ss_total else np.nan

    tukey = pairwise_tukeyhsd(endog=working[outcome], groups=working[grouping], alpha=alpha)
    pairwise = _tukey_to_records(tukey, _descriptives(working, grouping, outcome, group_order))
    return {
        "method": "classical_one_way_anova",
        "posthoc_method": "tukey_hsd",
        "descriptives": _descriptives(working, grouping, outcome, group_order),
        "omnibus": {
            "stat_name": "F",
            "df1": float(effect_row["df"]),
            "df2": float(residual_row["df"]),
            "statistic": float(effect_row["F"]),
            "p": float(effect_row["PR(>F)"]),
            "effect_size_name": "eta_squared",
            "effect_size": float(eta_sq),
        },
        "pairwise": pairwise,
    }


def _welch_anova(data: pd.DataFrame, grouping: str, outcome: str, group_order: list[str], alpha: float) -> dict[str, Any]:
    working = data[[grouping, outcome]].dropna().copy()
    working[grouping] = pd.Categorical(working[grouping], categories=group_order, ordered=True)
    anova = pg.welch_anova(data=working, dv=outcome, between=grouping)
    row = anova.iloc[0]
    p_key = "p-unc" if "p-unc" in row.index else "p_unc"
    games = pg.pairwise_gameshowell(data=working, dv=outcome, between=grouping)
    pairwise = _games_howell_to_records(games)
    return {
        "method": "welch_anova",
        "posthoc_method": "games_howell",
        "descriptives": _descriptives(working, grouping, outcome, group_order),
        "omnibus": {
            "stat_name": "F",
            "df1": float(row["ddof1"]),
            "df2": float(row["ddof2"]),
            "statistic": float(row["F"]),
            "p": float(row[p_key]),
            "effect_size_name": "partial_eta_squared",
            "effect_size": float(row.get("np2", np.nan)),
        },
        "pairwise": pairwise,
    }


def _tukey_to_records(tukey_result: Any, descriptives: dict[str, Any]) -> list[dict[str, Any]]:
    rows = tukey_result.summary().data[1:]
    records = []
    for row in rows:
        group_a, group_b, mean_diff, p_adj, lower, upper, reject = row
        records.append({
            "group_a": str(group_a),
            "group_b": str(group_b),
            "mean_a": descriptives[str(group_a)]["mean"],
            "mean_b": descriptives[str(group_b)]["mean"],
            "mean_diff": float(mean_diff),
            "se": None,
            "ci_low": float(lower),
            "ci_high": float(upper),
            "p_adj": float(p_adj),
            "significant": bool(reject),
        })
    return records


def _games_howell_to_records(games: pd.DataFrame) -> list[dict[str, Any]]:
    records = []
    for _, row in games.iterrows():
        mean_a_key = "mean(A)" if "mean(A)" in row.index else "mean_A"
        mean_b_key = "mean(B)" if "mean(B)" in row.index else "mean_B"
        ci = row["CI95%"] if "CI95%" in row.index else [np.nan, np.nan]
        records.append({
            "group_a": str(row["A"]),
            "group_b": str(row["B"]),
            "mean_a": float(row[mean_a_key]),
            "mean_b": float(row[mean_b_key]),
            "mean_diff": float(row["diff"]),
            "se": float(row["se"]),
            "ci_low": float(ci[0]) if not pd.isna(ci[0]) else None,
            "ci_high": float(ci[1]) if not pd.isna(ci[1]) else None,
            "p_adj": float(row["pval"]),
            "significant": bool(row["pval"] < 0.05),
        })
    return records
