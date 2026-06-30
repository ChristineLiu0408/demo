"""Workflow orchestration entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .analysis_runner import run_confirmed_analyses
from .figure_generator import create_combined_raincloud_figure
from .quality_check import run_quality_check
from .report_writer import write_business_report_docx, write_business_report_markdown
from .suitability_check import run_suitability_check
from .table_generator import build_mean_table, write_mean_table_csv
from .utils import load_yaml, project_path, write_text


def main() -> None:
    parser = argparse.ArgumentParser(description="AI statistical reporting workflow demo")
    parser.add_argument("--stage", choices=["check", "report"], default="check", help="Workflow stage to run.")
    parser.add_argument("--analysis-plan", default="config/analysis_plan.yaml", help="Path to the analysis plan YAML.")
    parser.add_argument("--decision-file", default=None, help="Path to the human review decision YAML.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated workflow outputs.")
    args = parser.parse_args()

    if args.stage == "check":
        result = run_suitability_check(analysis_plan_path=args.analysis_plan, output_dir=args.output_dir)
        print(f"Overall decision: {result['overall_decision']}")
        print(f"Wrote: {result['suitability_report']}")
        print(f"Wrote: {result['human_review_required']}")
        print("Workflow paused for human review. Formal reporting outputs were not generated.")
    elif args.stage == "report":
        result = run_report_stage(
            analysis_plan_path=args.analysis_plan,
            decision_path=args.decision_file,
            output_dir=args.output_dir,
        )
        print("Formal report workflow completed after human approval.")
        for label, path in result.items():
            print(f"{label}: {path}")


def run_report_stage(
    analysis_plan_path: str | Path = "config/analysis_plan.yaml",
    decision_path: str | Path | None = None,
    output_dir: str | Path = "outputs",
) -> dict[str, str]:
    output_dir = Path(output_dir)
    suitability = run_suitability_check(analysis_plan_path=analysis_plan_path, output_dir=output_dir)
    if suitability["overall_decision"] in {"diagnostic_only", "stop_analysis"}:
        raise RuntimeError(f"Formal reporting blocked by suitability decision: {suitability['overall_decision']}")

    plan = load_yaml(analysis_plan_path)
    decision_path = decision_path or plan.get("human_review", {}).get("decision_file") or "config/human_review_decision.yaml"
    results = run_confirmed_analyses(analysis_plan_path=analysis_plan_path, decision_path=decision_path)
    data = pd.read_csv(project_path(plan["dataset_path"]))
    mean_table = build_mean_table(results, plan)

    table_path = write_mean_table_csv(mean_table, output_dir / "mean_table_compact_letters.csv")
    figure_path = create_combined_raincloud_figure(data, results, plan, output_dir / "figure_combined_raincloud.png")
    markdown_path = write_business_report_markdown(results, plan, mean_table, figure_path, output_dir / "business_friendly_report_zh.md")
    docx_path = write_business_report_docx(results, plan, mean_table, figure_path, output_dir / "final_report.docx")
    json_path = write_text(output_dir / "analysis_results.json", json.dumps(_json_safe(results), ensure_ascii=False, indent=2))
    quality_path = run_quality_check(
        results,
        plan,
        {
            "analysis_results": json_path,
            "mean_table": table_path,
            "figure": figure_path,
            "markdown_report": markdown_path,
            "word_report": docx_path,
        },
        output_dir / "quality_check.md",
    )
    return {
        "suitability_report": str(suitability["suitability_report"]),
        "human_review_required": str(suitability["human_review_required"]),
        "analysis_results": str(json_path),
        "mean_table": str(table_path),
        "figure": str(figure_path),
        "markdown_report": str(markdown_path),
        "word_report": str(docx_path),
        "quality_check": str(quality_path),
    }


def _json_safe(value):
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


if __name__ == "__main__":
    main()
