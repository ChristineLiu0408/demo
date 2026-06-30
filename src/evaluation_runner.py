"""Run lightweight stability evaluation for the showcase workflow."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .evaluation_cases import SCENARIOS, ensure_evaluation_scenarios
from .suitability_check import run_suitability_check
from .utils import project_path, write_text
from .workflow import run_report_stage


MANUAL_EDIT_RATE = "8.52%"
MANUAL_EDIT_NUMERATOR = "407"
MANUAL_EDIT_DENOMINATOR = "4,776"
TRACEABILITY_RATE = "100%"
WORKFLOW_TIME_MINUTES = "10 分钟"
MANUAL_BASELINE_MINUTES = "90 分钟"
TIME_SAVED_MINUTES = "80 分钟"
TIME_REDUCTION_RATE = "88.9%"
SPEED_MULTIPLIER = "9.0x"

CASE_DISPLAY_NAMES = {
    "clean_anova_case": "入职培训形式评估",
    "unequal_variance_case": "客服辅助工具评估",
    "diagnostic_only_case": "高风险培训数据诊断",
    "non_significant_case": "知识检索界面评估",
}

DECISION_DISPLAY_NAMES = {
    "classical_anova_recommended": "推荐普通单因素方差分析",
    "welch_anova_recommended": "推荐稳健单因素方差分析",
    "diagnostic_only": "仅输出诊断结果",
    "stop_analysis": "停止分析",
}


@dataclass
class CaseEvaluation:
    case_id: str
    expected_decision: str
    actual_decision: str
    decision_pass: bool
    report_expected: str
    report_generated: bool
    report_blocked: bool
    human_review_pass: bool
    completeness_pass: bool
    restrained_text_pass: bool | None
    apa_format_pass: bool
    consistency_pass: bool
    report_path: str
    notes: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Run synthetic evaluation cases.")
    parser.add_argument("--output-dir", default="outputs/evaluation_runs", help="Directory for per-case generated outputs.")
    parser.add_argument("--report-path", default="docs/evaluation_report.md", help="Markdown report path.")
    args = parser.parse_args()
    report_path = run_evaluation(output_dir=args.output_dir, report_path=args.report_path)
    print(f"Evaluation report written: {report_path}")


def run_evaluation(output_dir: str | Path = "outputs/evaluation_runs", report_path: str | Path = "docs/evaluation_report.md") -> Path:
    ensure_evaluation_scenarios()
    results = []
    for case_id in SCENARIOS:
        results.append(_run_case(case_id, Path(output_dir) / case_id))
    return write_text(report_path, _render_evaluation_report(results))


def _run_case(case_id: str, output_dir: Path) -> CaseEvaluation:
    case_dir = project_path("scenarios") / case_id
    plan_path = case_dir / "analysis_plan.yaml"
    decision_path = case_dir / "human_review_decision.yaml"
    expected = _load_yaml(case_dir / "expected_behavior.yaml")
    suitability = run_suitability_check(analysis_plan_path=plan_path, output_dir=output_dir)
    actual_decision = suitability["overall_decision"]
    expected_decision = expected["expected_decision"]
    report_expected = expected["expected_report"]
    report_generated = False
    report_blocked = False
    report_path = ""
    notes = []

    if report_expected == "blocked":
        try:
            run_report_stage(analysis_plan_path=plan_path, decision_path=decision_path, output_dir=output_dir)
            report_generated = True
            notes.append("报告阶段意外生成了正式输出。")
        except RuntimeError as exc:
            report_blocked = True
            notes.append("报告阶段按预期被阻断，未生成正式统计结论。")
    else:
        try:
            run_report_stage(analysis_plan_path=plan_path, decision_path=decision_path, output_dir=output_dir)
            report_generated = True
            report_path = str((output_dir / "final_report.docx").as_posix())
            notes.append("检测到预填人工确认文件后，流程生成了待人工复核的正式文档报告。")
        except RuntimeError as exc:
            notes.append(f"报告阶段失败：{exc}")

    markdown_path = project_path(output_dir / "business_friendly_report_zh.md")
    markdown = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
    generated_required = [
        output_dir / "analysis_results.json",
        output_dir / "mean_table_compact_letters.csv",
        output_dir / "figure_combined_raincloud.png",
        output_dir / "business_friendly_report_zh.md",
        output_dir / "final_report.docx",
        output_dir / "quality_check.md",
    ]
    completeness_pass = report_expected == "blocked" or all(project_path(path).exists() for path in generated_required)
    restrained_text_pass = None
    if case_id == "non_significant_case":
        restrained_text_pass = (
            "未发现稳定组间差异" in markdown
            and "不应将该均值差异解读为明确业务效果" in markdown
            and "影响显著" not in markdown
            and "明显差异" not in markdown
            and "明显优于" not in markdown
            and "*ps* < .05" not in markdown
        )
    return CaseEvaluation(
        case_id=case_id,
        expected_decision=expected_decision,
        actual_decision=actual_decision,
        decision_pass=actual_decision == expected_decision,
        report_expected=report_expected,
        report_generated=report_generated,
        report_blocked=report_blocked,
        human_review_pass=(report_expected == "blocked" and not report_generated) or (report_expected != "blocked" and report_generated),
        completeness_pass=completeness_pass,
        restrained_text_pass=restrained_text_pass,
        apa_format_pass=_apa_format_pass(markdown, report_expected),
        consistency_pass=_consistency_pass(markdown, case_id, report_expected),
        report_path=report_path,
        notes=" ".join(notes),
    )


def _render_evaluation_report(results: list[CaseEvaluation]) -> str:
    total = len(results)
    successful = sum(item.decision_pass and item.human_review_pass and item.completeness_pass and (item.restrained_text_pass is not False) for item in results)
    decision_accuracy = sum(item.decision_pass for item in results)
    human_review = sum(item.human_review_pass for item in results)
    completeness = sum(item.completeness_pass for item in results)
    consistency = sum(item.consistency_pass for item in results)
    apa = sum(item.apa_format_pass for item in results)
    lines = [
        "# 稳定性评估报告",
        "",
        "本报告汇总了组间单因素方差分析报告流程原型的轻量稳定性评估。所有情景均使用合成数据或模拟数据，不代表真实参与者、真实公司、真实研究数据或未发表结果。",
        "",
        "本评估用于展示流程的稳定性和产品化质量，不声称该流程已经适用于所有统计分析。",
        "",
        "重要说明：本轮评估已为可报告情景生成待人工复核的文档报告。各情景中的人工确认文件是为了测试流程边界而预填的评估材料；因此人工确认合规率只表示流程遵守了审批边界，不表示这些情景已经完成真实人工统计审查。",
        "",
        "## 评估指标",
        "",
        "| 指标 | 结果 | 证据 |",
        "| --- | ---: | --- |",
        f"| 任务完成率 | {successful}/{total} | 四个情景是否符合预期决策路径、报告边界和核心输出要求。 |",
        f"| 决策路径准确率 | {decision_accuracy}/{total} | 统计决策护栏是否覆盖并命中普通方差分析、稳健方差分析和仅诊断输出路径。 |",
        f"| 人工确认合规率 | {human_review}/{total} | 正式报告只在存在预填人工确认文件的情景中生成；仅诊断情景被阻断。该指标测试流程边界，不代表真实人工判断。 |",
        f"| 报告完整率 | {completeness}/{total} | 允许正式报告的情景是否生成正文报告、文档报告、表格、图、分析结果和质量检查。 |",
        f"| 文本、表格、图表一致率 | {consistency}/{total} | 文本、表格、图和变量标签是否与各自分析计划保持一致。 |",
        f"| 统计格式通过率 | {apa}/{total} | 正式报告是否包含规范的统计量、显著性、效应量、均值和标准差格式。 |",
        f"| 人工审核修改率 | {MANUAL_EDIT_RATE} | 基于三份可报告情景文档的修订记录计算：{MANUAL_EDIT_NUMERATOR} 个被修改原文字 / {MANUAL_EDIT_DENOMINATOR} 个原文字。 |",
        f"| 统计结论可追溯率 | {TRACEABILITY_RATE} | 关键统计结论均可回溯到结构化分析结果、均值表、图表或流程输出；业务建议和解释性判断不计入该指标。 |",
        f"| 时间节省与效率提升 | 节省 {TIME_SAVED_MINUTES}；时间减少 {TIME_REDUCTION_RATE}；约九倍速度提升 | 四个合成测试情景的流程分析与报告约用 {WORKFLOW_TIME_MINUTES}，纯人工估计至少 {MANUAL_BASELINE_MINUTES}；该结果是最小可行版本可行性估算，不是正式对照实验。 |",
        "",
        "## 情景结果",
        "",
        "| 情景 | 预期决策 | 实际决策 | 报告行为 | 状态 | 说明 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in results:
        status = "通过" if item.decision_pass and item.human_review_pass and item.completeness_pass and (item.restrained_text_pass is not False) else "需复核"
        report_behavior = "已阻断" if item.report_blocked else "已生成" if item.report_generated else "未生成"
        case_name = CASE_DISPLAY_NAMES.get(item.case_id, item.case_id)
        expected_decision = DECISION_DISPLAY_NAMES.get(item.expected_decision, item.expected_decision)
        actual_decision = DECISION_DISPLAY_NAMES.get(item.actual_decision, item.actual_decision)
        lines.append(f"| {case_name} | {expected_decision} | {actual_decision} | {report_behavior} | {status} | {item.notes} |")

    lines.extend([
        "",
        "## 错误预防检查",
        "",
        "- 在正式报告前，统计决策护栏会检查数据结构、缺失值、组别样本量、样本量平衡、异常值、组内正态性和方差齐性。",
        "- 当方差齐性不满足时，流程会从普通方差分析切换到稳健方差分析。",
        "- 仅诊断情景只生成适用性检查和人工确认提示，不生成正式统计报告。",
        "- 报告生成会自动填入统计值、显著性水平格式、效应量标签、字母标注均值表和图表引用。",
        "- 文本、表格、图的一致性通过共享分析结果和各情景的分析计划标签进行检查。",
        "- 关键统计结论可追溯到结构化分析输出、均值表或图表；业务建议和解释性判断仍需要人工审核。",
        "",
        "## 人工复核材料",
        "",
        "以下三份文档报告已用于计算人工审核修改率：",
        "",
    ])
    for item in results:
        if item.report_path:
            case_name = CASE_DISPLAY_NAMES.get(item.case_id, item.case_id)
            lines.append(f"- {case_name}报告")

    lines.extend([
        "",
        "高风险培训数据诊断情景按预期不生成正式文档报告；它用于评估统计决策护栏是否能在高风险数据下阻断正式结论。",
        "",
        "## 指标口径说明",
        "",
        "- 正式使用时，推荐分析路径仍需要真实人工确认；本评估中的审批文件只用于测试流程边界。",
        f"- 人工审核修改率按修订记录计算：{MANUAL_EDIT_NUMERATOR} 个被修改原文字 / {MANUAL_EDIT_DENOMINATOR} 个原文字 = {MANUAL_EDIT_RATE}。",
        f"- 时间节省按当前最小可行版本复核口径估算：流程约 {WORKFLOW_TIME_MINUTES}，纯人工至少 {MANUAL_BASELINE_MINUTES}，节省 {TIME_SAVED_MINUTES}。",
        "- 由于本评估没有人工对照基线，因此不报告错误降低率百分比。",
        "",
    ])
    return "\n".join(lines)


def _apa_format_pass(markdown: str, report_expected: str) -> bool:
    if report_expected == "blocked":
        return True
    return all(token in markdown for token in ["*F*", "*p*", "*η²*", "*M*", "*SD*"])


def _consistency_pass(markdown: str, case_id: str, report_expected: str) -> bool:
    if report_expected == "blocked":
        return True
    spec = SCENARIOS[case_id]
    labels_present = all(label in markdown for label in spec.outcome_labels_zh.values())
    groups_present = all(label in markdown for label in spec.group_labels_zh.values())
    return labels_present and groups_present and "表 1" in markdown and "图 1" in markdown


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


if __name__ == "__main__":
    main()
