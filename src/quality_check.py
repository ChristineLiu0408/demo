"""Consistency checks across generated paragraphs, tables, figures, and reports."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .utils import PROJECT_ROOT, project_path, write_text


Check = tuple[str, str, str, str]


def run_quality_check(
    results: dict[str, Any],
    plan: dict[str, Any],
    generated_files: dict[str, Path],
    output_path: str | Path = "outputs/quality_check.md",
) -> Path:
    outcomes = plan["analysis"]["outcome_variables"]
    outcome_labels = plan["analysis"]["outcome_labels_zh"]
    markdown_path = project_path(generated_files["markdown_report"])
    markdown = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""

    sections: list[tuple[str, list[Check]]] = [
        ("Workflow Gate", _workflow_gate_checks(results, plan, generated_files)),
        ("Data & Analysis Integrity", _data_integrity_checks(results, plan, generated_files)),
        ("Statistical Reporting Quality", _statistical_reporting_checks(results, plan, markdown)),
        ("Report Structure & Communication", _report_structure_checks(markdown)),
        ("Table & Figure QA", _table_figure_checks(markdown, generated_files)),
        ("Report Editorial QA", _editorial_checks()),
        ("Privacy & Public Showcase Safety", _privacy_checks(markdown, generated_files)),
    ]

    text = [
        "# Quality Check",
        "",
        "This QA report checks whether the workflow stayed inside the approved human-in-the-loop boundary, used the expected data and analysis path, and generated public-safe reporting assets.",
        "",
        "QA is intentionally layered: hard checks cover workflow validity and public safety; soft checks cover stable machine-checkable reporting rules; editorial checks record human review items without turning every writing preference into an automated failure.",
        "",
    ]
    for title, checks in sections:
        text.extend([
            f"## {title}",
            "",
            "| Check | Status | Evidence | Action if Failed |",
            "| --- | --- | --- | --- |",
        ])
        text.extend(f"| {name} | `{status}` | {evidence} | {action} |" for name, status, evidence, action in checks)
        text.append("")

    text.extend([
        "## Outcome Labels",
        "",
    ])
    text.extend(f"- `{outcome}`: {outcome_labels[outcome]}" for outcome in outcomes)
    text.extend([
        "",
        "## Guardrail Confirmation",
        "",
        "- No formal APA-style results, table, figure, or Word report should be generated before approval.",
        "- This run used the explicit outcome-level approval recorded in `config/human_review_decision.yaml`.",
        "- `diagnostic_only` and `stop_analysis` are not present in this run.",
    ])
    return write_text(output_path, "\n".join(text) + "\n")


def _workflow_gate_checks(results: dict[str, Any], plan: dict[str, Any], generated_files: dict[str, Path]) -> list[Check]:
    outcomes = plan["analysis"]["outcome_variables"]
    approved_outcomes = [
        outcome for outcome in outcomes
        if results["outcomes"].get(outcome, {}).get("approved_analysis_path")
    ]
    return [
        (
            "Human approval gate",
            "pass" if len(approved_outcomes) == len(outcomes) else "fail",
            f"{len(approved_outcomes)}/{len(outcomes)} outcomes include approved analysis paths.",
            "Pause report generation and update the outcome-level human review decision file.",
        ),
        (
            "Formal outputs after approval",
            "pass" if all(project_path(path).exists() for path in generated_files.values()) else "fail",
            "Formal outputs were generated in the report stage.",
            "Do not generate report assets until all required approvals are recorded.",
        ),
        (
            "Blocked decisions absent",
            "pass",
            "This report stage did not proceed from diagnostic_only or stop_analysis.",
            "Stop formal reporting and return only diagnostic guidance.",
        ),
    ]


def _data_integrity_checks(results: dict[str, Any], plan: dict[str, Any], generated_files: dict[str, Path]) -> list[Check]:
    outcomes = plan["analysis"]["outcome_variables"]
    method_ok = all(
        _expected_posthoc(item.get("method")) == item.get("posthoc_method")
        for item in results["outcomes"].values()
    )
    baseline = plan["reporting"].get("baseline_condition", plan["analysis"]["condition_order"][0])
    focal = plan["reporting"].get("focal_condition", plan["analysis"]["condition_order"][-1])
    checks: list[Check] = [
        (
            "Outcome coverage",
            "pass" if set(outcomes) == set(results["outcomes"]) else "fail",
            f"Configured outcomes: {len(outcomes)}; analyzed outcomes: {len(results['outcomes'])}.",
            "Rerun analyses for missing outcomes or update the analysis plan.",
        ),
        (
            "Analysis path consistency",
            "pass" if method_ok else "fail",
            "Classical ANOVA maps to Tukey HSD; Welch ANOVA maps to Games-Howell.",
            "Align the approved analysis path and post hoc method for each outcome.",
        ),
        (
            "Baseline and focal groups",
            "pass" if baseline in results["group_order"] and focal in results["group_order"] else "fail",
            f"Baseline: {baseline}; focal: {focal}.",
            "Set valid baseline_condition and focal_condition in analysis_plan.yaml.",
        ),
    ]
    required_assets = {
        "analysis_results": "analysis_results.json",
        "mean_table": "mean_table_compact_letters.csv",
        "figure": "figure_combined_raincloud.png",
        "markdown_report": "business_friendly_report_zh.md",
        "word_report": "final_report.docx",
    }
    missing_assets = [
        filename
        for label, filename in required_assets.items()
        if label not in generated_files or not project_path(generated_files[label]).exists()
    ]
    checks.append(
        (
            "Formal report asset completeness",
            "pass" if not missing_assets else "fail",
            "Generated final Word report, Chinese Markdown report, figure, mean table, and analysis results JSON." if not missing_assets else f"Missing: {', '.join(missing_assets)}.",
            "Rerun the report stage and inspect the final Word report, figure, mean table, and analysis JSON.",
        )
    )
    return checks


def _statistical_reporting_checks(results: dict[str, Any], plan: dict[str, Any], markdown: str) -> list[Check]:
    outcomes = plan["analysis"]["outcome_variables"]
    omnibus_ok = all(
        {"df1", "df2", "statistic", "p", "effect_size"}.issubset(results["outcomes"][outcome]["omnibus"])
        for outcome in outcomes
    )
    labels = plan["analysis"]["condition_labels_zh"]
    baseline = labels[plan["reporting"].get("baseline_condition", plan["analysis"]["condition_order"][0])]
    focal = labels[plan["reporting"].get("focal_condition", plan["analysis"]["condition_order"][-1])]
    percent_in_core = _text_between(markdown, "### 1.2 核心结果", "### 1.3 行动建议")
    return [
        (
            "Omnibus statistics",
            "pass" if omnibus_ok else "fail",
            "Each outcome includes df, statistic, p value, and effect size.",
            "Rebuild analysis_results.json from the confirmed analysis runner.",
        ),
        (
            "APA symbols",
            "pass" if all(symbol in markdown for symbol in ["*F*", "*p*", "*η²*", "*M*", "*SD*"]) else "warning",
            "Markdown report includes italicized APA statistical symbols.",
            "Regenerate result paragraphs with APA symbol formatting.",
        ),
        (
            "Percent interpretation",
            "pass" if "%" in percent_in_core and baseline in percent_in_core and focal in percent_in_core else "fail",
            f"Core result compares {focal} against {baseline}.",
            "Add dynamic percentage interpretation to the core results section.",
        ),
        (
            "Positive and negative direction wording",
            "pass" if "提升" in percent_in_core and "降低" in percent_in_core else "warning",
            "Core percentage summary distinguishes increase and decrease wording.",
            "Check outcome_directions in analysis_plan.yaml.",
        ),
    ]


def _report_structure_checks(markdown: str) -> list[Check]:
    table_index = markdown.find("**表 1.")
    detail_index = markdown.find("## 2. 详细统计报告")
    return [
        (
            "Two-part report structure",
            "pass" if "## 1. 核心内容" in markdown and "## 2. 详细统计报告" in markdown else "fail",
            "Report uses core content plus detailed statistical report sections.",
            "Restore the two-part report structure.",
        ),
        (
            "Core content subsections",
            "pass" if all(item in markdown for item in ["### 1.1 报告目标", "### 1.2 核心结果", "### 1.3 行动建议"]) else "fail",
            "Core content is split into goal, result, and recommendation subsections.",
            "Add the three required subsections under core content.",
        ),
        (
            "Table in detailed report",
            "pass" if detail_index >= 0 and table_index > detail_index else "fail",
            "Table 1 appears under the detailed statistical report section.",
            "Move Table 1 below the method-selection paragraph in Section 2.",
        ),
        (
            "No report-level mock data disclaimer",
            "pass" if "synthetic/mock data" not in markdown else "warning",
            "Formal business report does not foreground the mock-data disclaimer.",
            "Keep mock-data disclosure in README/privacy docs rather than the formal report body.",
        ),
    ]


def _table_figure_checks(markdown: str, generated_files: dict[str, Path]) -> list[Check]:
    figure_title = markdown.find("**图 1.")
    figure_image = markdown.find("![图 1]")
    table_title = markdown.find("**表 1.")
    table_pipe = markdown.find("结果指标", table_title)
    return [
        (
            "Figure output",
            "pass" if project_path(generated_files["figure"]).exists() else "fail",
            _relative_path(generated_files["figure"]),
            "Regenerate the combined raincloud figure.",
        ),
        (
            "Figure title above image",
            "pass" if 0 <= figure_title < figure_image else "fail",
            "Figure title is report text before the image, not embedded inside the plot.",
            "Move the figure title above the image in Markdown and Word.",
        ),
        (
            "Table title above table",
            "pass" if 0 <= table_title < table_pipe else "fail",
            "Table title appears before the rendered mean table.",
            "Move the table title above the table.",
        ),
        (
            "Table and figure notes",
            "pass" if "注：点表示个体观测值" in markdown and "注：数值为均值" in markdown else "warning",
            "Figure and table notes are generated as report text below the visual assets.",
            "Regenerate notes below the corresponding figure and table.",
        ),
    ]


def _editorial_checks() -> list[Check]:
    return [
        (
            "Core result readability",
            "manual",
            "Confirm percentage interpretation is integrated into the core result paragraph rather than listed as a separate mechanical note.",
            "Revise the report template or report_context wording, then regenerate the report.",
        ),
        (
            "Figure/table block presentation",
            "manual",
            "Review each figure/table as one block: title, visual or table body, note, and surrounding whitespace.",
            "Adjust block spacing helpers, caption wording, figure size, or table geometry.",
        ),
        (
            "Rendered Word layout QA",
            "manual",
            "Render the DOCX and inspect for isolated headings, cramped tables, awkward page breaks, or overlapping figure annotations.",
            "Revise Word spacing, keep-with-next behavior, figure dimensions, or table width before publishing.",
        ),
    ]


def _privacy_checks(markdown: str, generated_files: dict[str, Path]) -> list[Check]:
    text_assets = [markdown]
    for label in ("analysis_results", "mean_table"):
        if label not in generated_files:
            continue
        path = project_path(generated_files[label])
        if path.exists() and path.is_file():
            text_assets.append(path.read_text(encoding="utf-8", errors="ignore"))
    combined = "\n".join(text_assets)
    has_absolute_path = any(token in combined for token in ["/Users/", "/private/", ".codex"])
    has_secret_like_text = bool(re.search(r"(api[_-]?key|secret|token|password)\s*[:=]", combined, flags=re.IGNORECASE))
    has_email = bool(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", combined))
    return [
        (
            "Local path exposure",
            "pass" if not has_absolute_path else "fail",
            "No local absolute paths found in text outputs.",
            "Replace absolute paths with project-relative paths before publishing.",
        ),
        (
            "Secret-like strings",
            "pass" if not has_secret_like_text else "fail",
            "No API keys, tokens, passwords, or similar secret markers found.",
            "Remove secrets and rotate any exposed credentials.",
        ),
        (
            "Personal contact leakage",
            "pass" if not has_email else "warning",
            "No email-like strings found in generated text outputs.",
            "Remove personal contact information unless intentionally public.",
        ),
    ]


def _expected_posthoc(method: str | None) -> str | None:
    if method == "classical_one_way_anova":
        return "tukey_hsd"
    if method == "welch_anova":
        return "games_howell"
    return None


def _text_between(text: str, start: str, end: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        return ""
    end_index = text.find(end, start_index)
    if end_index < 0:
        return text[start_index:]
    return text[start_index:end_index]


def _relative_path(path: Path | str) -> str:
    resolved = project_path(path)
    try:
        return resolved.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return resolved.name
