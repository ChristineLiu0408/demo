"""Synthetic evaluation case generation for the showcase workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from .utils import project_path


@dataclass(frozen=True)
class ScenarioSpec:
    case_id: str
    title: str
    business_question: str
    grouping_variable: str
    group_order: list[str]
    group_labels_zh: dict[str, str]
    outcome_variables: list[str]
    outcome_labels_zh: dict[str, str]
    outcome_directions: dict[str, str]
    expected_decision: str
    expected_report: str
    baseline_condition: str
    focal_condition: str
    report_context: dict[str, Any]


SCENARIOS: dict[str, ScenarioSpec] = {
    "clean_anova_case": ScenarioSpec(
        case_id="clean_anova_case",
        title="员工入职培训形式效果评估报告",
        business_question="不同入职培训形式是否会影响新员工的学习效果、上手信心和培训负担感。",
        grouping_variable="onboarding_training_format",
        group_order=["Reading_Materials", "Recorded_Video", "Live_Workshop", "Mentor_Guided"],
        group_labels_zh={
            "Reading_Materials": "阅读材料",
            "Recorded_Video": "录播课程",
            "Live_Workshop": "直播工作坊",
            "Mentor_Guided": "导师带教",
        },
        outcome_variables=["learning_effectiveness", "onboarding_confidence", "training_burden"],
        outcome_labels_zh={
            "learning_effectiveness": "学习效果",
            "onboarding_confidence": "上手信心",
            "training_burden": "培训负担感",
        },
        outcome_directions={
            "learning_effectiveness": "positive",
            "onboarding_confidence": "positive",
            "training_burden": "negative",
        },
        expected_decision="classical_anova_recommended",
        expected_report="complete",
        baseline_condition="Reading_Materials",
        focal_condition="Mentor_Guided",
        report_context={
            "scenario_label": "入职培训形式评估",
            "participant_label": "新员工",
            "figure_title": "图 1. 不同入职培训形式的效果",
            "overview_sentence": "本次评估比较了{group_labels}在{outcome_list}上的差异，以支持{decision_context}。具体而言，每种入职培训形式均使用 synthetic/mock data 构建为独立组。",
            "questions": [
                "不同入职培训形式是否影响学习效果、上手信心和培训负担感？",
                "哪种入职培训形式对应更理想的新员工上手体验？",
            ],
            "core_findings": [
                "第一，不同入职培训形式之间存在清晰差异。",
                "第二，导师带教整体表现更好，既对应更高的学习效果和上手信心，也对应更低的培训负担感。",
            ],
            "implication_sentence": "这些结果说明，结构化的人际支持仍然是入职培训体验中的关键资源。示例图见图1。",
            "action_recommendations": [
                "后续可以优先保留导师带教中的高价值环节，并评估其规模化成本。",
                "如果需要降低培训资源投入，可以把导师带教拆解为标准化材料、录播课程和关键节点辅导的组合方案。",
            ],
        },
    ),
    "unequal_variance_case": ScenarioSpec(
        case_id="unequal_variance_case",
        title="客服辅助工具试点效果评估报告",
        business_question="客服团队使用不同辅助工具时，处理效率、服务信心和认知负荷是否不同。",
        grouping_variable="service_support_tool",
        group_order=["No_Tool", "Knowledge_Base", "Chatbot_Copilot", "Agent_Copilot"],
        group_labels_zh={
            "No_Tool": "无辅助工具",
            "Knowledge_Base": "知识库辅助",
            "Chatbot_Copilot": "对话助手辅助",
            "Agent_Copilot": "智能体助手辅助",
        },
        outcome_variables=["resolution_efficiency", "service_confidence", "cognitive_load"],
        outcome_labels_zh={
            "resolution_efficiency": "处理效率",
            "service_confidence": "服务信心",
            "cognitive_load": "认知负荷",
        },
        outcome_directions={
            "resolution_efficiency": "positive",
            "service_confidence": "positive",
            "cognitive_load": "negative",
        },
        expected_decision="welch_anova_recommended",
        expected_report="complete",
        baseline_condition="No_Tool",
        focal_condition="Agent_Copilot",
        report_context={
            "scenario_label": "客服辅助工具试点",
            "participant_label": "客服人员",
            "figure_title": "图 1. 不同客服辅助工具的效果",
            "overview_sentence": "本次评估比较了{group_labels}在{outcome_list}上的差异，以支持{decision_context}。该情景用于检验 workflow 是否能在方差齐性不满足时切换统计路径。",
            "questions": [
                "不同客服辅助工具是否影响处理效率、服务信心和认知负荷？",
                "当组间方差不齐时，workflow 是否会切换到更合适的 Welch ANOVA 路径？",
            ],
            "core_findings": [
                "第一，客服辅助工具与多个服务表现指标相关。",
                "第二，由于组间方差不齐，本轮分析采用 Welch ANOVA 和 Games-Howell 事后比较，而不是普通单因素方差分析。",
            ],
            "implication_sentence": "这些结果展示了 workflow 在方法选择上的 guardrail 价值。示例图见图1。",
            "action_recommendations": [
                "后续评估客服工具时，应同时关注均值改善和不同工具带来的结果波动。",
                "如果某类工具效果波动较大，建议进一步拆分使用人群、问题类型和培训熟练度。",
            ],
        },
    ),
    "diagnostic_only_case": ScenarioSpec(
        case_id="diagnostic_only_case",
        title="培训方案效果评估数据诊断报告",
        business_question="不同培训方案是否影响员工知识掌握、迁移信心和培训疲劳；但当前数据质量是否足以支持正式结论。",
        grouping_variable="training_format",
        group_order=["Self_Study", "Live_Workshop", "Blended_Coaching", "AI_Tutor"],
        group_labels_zh={
            "Self_Study": "自学材料",
            "Live_Workshop": "直播培训",
            "Blended_Coaching": "混合辅导",
            "AI_Tutor": "AI导师辅助",
        },
        outcome_variables=["knowledge_mastery", "transfer_confidence", "training_fatigue"],
        outcome_labels_zh={
            "knowledge_mastery": "知识掌握",
            "transfer_confidence": "迁移信心",
            "training_fatigue": "培训疲劳",
        },
        outcome_directions={
            "knowledge_mastery": "positive",
            "transfer_confidence": "positive",
            "training_fatigue": "negative",
        },
        expected_decision="diagnostic_only",
        expected_report="blocked",
        baseline_condition="Self_Study",
        focal_condition="AI_Tutor",
        report_context={
            "scenario_label": "培训方案高风险数据检查",
            "participant_label": "员工",
            "figure_title": "图 1. 不同培训方案的效果",
            "overview_sentence": "本次评估比较了{group_labels}在{outcome_list}上的差异，以支持{decision_context}。该情景故意使用高风险 synthetic/mock data，用于检验 workflow 是否会阻止正式统计结论。",
            "questions": [
                "当前数据质量是否足以支持培训方案效果结论？",
                "当样本量和数据质量风险较高时，workflow 是否会停止正式报告生成？",
            ],
            "core_findings": [
                "第一，当前数据只适合进行诊断，不适合自动生成正式业务结论。",
                "第二，后续应优先修复样本量、缺失值或异常值问题，再重新进入正式分析。",
            ],
            "implication_sentence": "该情景用于展示 workflow 的风险拦截能力。",
            "action_recommendations": [
                "在正式评估培训方案前，应补足有效样本并核查异常观测来源。",
                "如果数据结构确认无误，再重新运行 suitability check 并由人工确认分析路径。",
            ],
        },
    ),
    "non_significant_case": ScenarioSpec(
        case_id="non_significant_case",
        title="知识检索工具试点效果评估报告",
        business_question="不同知识检索界面是否能改善员工查找信息的效率、决策信心和费力程度。",
        grouping_variable="knowledge_search_interface",
        group_order=["Standard_Search", "Tagged_Knowledge_Base", "Guided_Workflow", "AI_Summary_Interface"],
        group_labels_zh={
            "Standard_Search": "标准搜索",
            "Tagged_Knowledge_Base": "标签知识库",
            "Guided_Workflow": "引导式流程",
            "AI_Summary_Interface": "AI摘要界面",
        },
        outcome_variables=["search_efficiency", "decision_confidence", "perceived_effort"],
        outcome_labels_zh={
            "search_efficiency": "查找效率",
            "decision_confidence": "决策信心",
            "perceived_effort": "感知费力程度",
        },
        outcome_directions={
            "search_efficiency": "positive",
            "decision_confidence": "positive",
            "perceived_effort": "negative",
        },
        expected_decision="classical_anova_recommended",
        expected_report="complete_restrained",
        baseline_condition="Standard_Search",
        focal_condition="AI_Summary_Interface",
        report_context={
            "scenario_label": "知识检索工具试点",
            "participant_label": "员工",
            "figure_title": "图 1. 不同知识检索界面的效果",
            "overview_sentence": "本次评估比较了{group_labels}在{outcome_list}上的差异，以支持{decision_context}。该情景用于检验 workflow 是否能在非显著结果下保持报告克制。",
            "questions": [
                "不同知识检索界面是否改善查找效率、决策信心和感知费力程度？",
                "当组间差异不稳定时，workflow 是否避免过度解读？",
            ],
            "core_findings": [
                "第一，不同知识检索界面之间没有出现稳定组间差异。",
                "第二，本轮结果不支持直接判断某一种界面优于其他界面。",
            ],
            "implication_sentence": "这些结果说明，当前试点更适合继续收集使用过程数据，而不是立即做大规模推广判断。示例图见图1。",
            "action_recommendations": [
                "后续可以扩大样本，并补充真实任务耗时、搜索成功率和用户访谈。",
                "在缺少稳定差异证据前，不建议仅依据当前均值差异决定工具替换。",
            ],
        },
    ),
}


def ensure_evaluation_scenarios() -> list[Path]:
    """Create reproducible synthetic scenario files under scenarios/."""
    written = []
    for case_id, spec in SCENARIOS.items():
        case_dir = project_path("scenarios") / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        data = _generate_data(spec)
        data_path = case_dir / "data.csv"
        data.to_csv(data_path, index=False)
        _write_yaml(case_dir / "analysis_plan.yaml", _analysis_plan(spec, data_path))
        _write_yaml(case_dir / "human_review_decision.yaml", _human_review_decision(spec))
        _write_yaml(case_dir / "expected_behavior.yaml", _expected_behavior(spec))
        _write_readme(case_dir / "README.md", spec)
        written.append(case_dir)
    return written


def _generate_data(spec: ScenarioSpec) -> pd.DataFrame:
    rng = np.random.default_rng(_seed(spec.case_id))
    if spec.case_id == "clean_anova_case":
        return _balanced_case(spec, rng, {
            "learning_effectiveness": [3.85, 4.25, 4.70, 5.15],
            "onboarding_confidence": [3.70, 4.15, 4.60, 5.05],
            "training_burden": [5.25, 4.85, 4.35, 3.90],
        }, [0.68, 0.68, 0.68, 0.68], 50)
    if spec.case_id == "unequal_variance_case":
        return _balanced_case(spec, rng, {
            "resolution_efficiency": [3.95, 4.35, 4.80, 5.20],
            "service_confidence": [3.80, 4.25, 4.65, 5.05],
            "cognitive_load": [5.25, 4.85, 4.40, 3.95],
        }, [0.35, 0.48, 0.78, 1.20], 50)
    if spec.case_id == "diagnostic_only_case":
        return _balanced_case(spec, rng, {
            "knowledge_mastery": [3.80, 4.10, 4.45, 4.75],
            "transfer_confidence": [3.75, 4.05, 4.35, 4.65],
            "training_fatigue": [5.10, 4.95, 4.75, 4.50],
        }, [0.85, 0.95, 1.05, 1.10], 8)
    if spec.case_id == "non_significant_case":
        return _matched_null_case(spec, rng, {
            "search_efficiency": [4.20, 4.22, 4.25, 4.24],
            "decision_confidence": [4.10, 4.12, 4.13, 4.11],
            "perceived_effort": [4.50, 4.47, 4.45, 4.46],
        }, 0.72, 50)
    raise ValueError(f"Unknown scenario: {spec.case_id}")


def _balanced_case(spec: ScenarioSpec, rng: np.random.Generator, means: dict[str, list[float]], sds: list[float], n: int) -> pd.DataFrame:
    rows = []
    for group_index, group in enumerate(spec.group_order):
        for item_index in range(n):
            row = {
                "participant_id": f"{spec.case_id[:3].upper()}_{group_index + 1}_{item_index + 1:03d}",
                spec.grouping_variable: group,
            }
            for outcome in spec.outcome_variables:
                value = rng.normal(means[outcome][group_index], sds[group_index])
                row[outcome] = round(float(np.clip(value, 1, 7)), 2)
            rows.append(row)
    return pd.DataFrame(rows)


def _matched_null_case(spec: ScenarioSpec, rng: np.random.Generator, means: dict[str, list[float]], sd: float, n: int) -> pd.DataFrame:
    base_values = {
        outcome: rng.normal(0, sd, n)
        for outcome in spec.outcome_variables
    }
    rows = []
    for group_index, group in enumerate(spec.group_order):
        for item_index in range(n):
            row = {
                "participant_id": f"{spec.case_id[:3].upper()}_{group_index + 1}_{item_index + 1:03d}",
                spec.grouping_variable: group,
            }
            for outcome in spec.outcome_variables:
                centered = base_values[outcome][item_index] - base_values[outcome].mean()
                value = means[outcome][group_index] + centered
                row[outcome] = round(float(np.clip(value, 1, 7)), 2)
            rows.append(row)
    return pd.DataFrame(rows)


def _analysis_plan(spec: ScenarioSpec, data_path: Path) -> dict[str, Any]:
    data_path_rel = data_path.relative_to(project_path(".")).as_posix()
    return {
        "project_name": "ai-stat-report-workflow-demo",
        "dataset_path": data_path_rel,
        "analysis": {
            "analysis_type": "one_way_anova",
            "grouping_variable": spec.grouping_variable,
            "grouping_variable_label_zh": _grouping_label(spec),
            "condition_order": spec.group_order,
            "condition_labels_zh": spec.group_labels_zh,
            "outcome_variables": spec.outcome_variables,
            "outcome_labels_zh": spec.outcome_labels_zh,
            "outcome_directions": spec.outcome_directions,
        },
        "reporting": {
            "analysis_title": spec.title,
            "decision_context": _strip_sentence_end(spec.business_question),
            "baseline_condition": spec.baseline_condition,
            "focal_condition": spec.focal_condition,
            "report_context": spec.report_context,
            "alpha": 0.05,
            "table_format": "compact_letter_mean_table",
            "figure_type": "combined_raincloud",
            "figure_style": "color_manuscript_ready",
            "figure_show_all_significant_brackets": True,
            "word_fonts": {
                "east_asian": "SimSun",
                "latin": "Times New Roman",
            },
            "output_word_report": True,
        },
        "human_review": {
            "required_before_analysis": True,
            "decision_file": f"scenarios/{spec.case_id}/human_review_decision.yaml",
        },
    }


def _human_review_decision(spec: ScenarioSpec) -> dict[str, Any]:
    if spec.expected_decision == "welch_anova_recommended":
        analysis_path = "welch_anova"
        posthoc = "games_howell"
    else:
        analysis_path = "classical_anova"
        posthoc = "tukey_hsd"
    return {
        "approval_status": "approved" if spec.expected_report != "blocked" else "not_approved",
        "reviewer_note": "Synthetic evaluation case decision file. Not based on real participants, companies, or research data.",
        "outcome_decisions": {
            outcome: {
                "approval_status": "approved" if spec.expected_report != "blocked" else "not_approved",
                "approved_analysis_path": analysis_path,
                "approved_posthoc_method": posthoc,
            }
            for outcome in spec.outcome_variables
        },
    }


def _expected_behavior(spec: ScenarioSpec) -> dict[str, Any]:
    return {
        "case_id": spec.case_id,
        "expected_decision": spec.expected_decision,
        "expected_report": spec.expected_report,
        "synthetic_data_only": True,
        "business_scenario": spec.business_question,
    }


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _write_readme(path: Path, spec: ScenarioSpec) -> None:
    text = [
        f"# {spec.case_id}",
        "",
        "This scenario uses synthetic/mock data only. It does not represent real participants, real companies, real research data, or unpublished results.",
        "",
        f"- Business scenario: {spec.business_question}",
        f"- Grouping variable: `{spec.grouping_variable}`",
        f"- Groups: {', '.join(spec.group_labels_zh[group] for group in spec.group_order)}",
        f"- Outcomes: {', '.join(spec.outcome_labels_zh[outcome] for outcome in spec.outcome_variables)}",
        f"- Expected decision: `{spec.expected_decision}`",
        f"- Expected report behavior: `{spec.expected_report}`",
        "",
    ]
    path.write_text("\n".join(text), encoding="utf-8")


def _grouping_label(spec: ScenarioSpec) -> str:
    labels = {
        "clean_anova_case": "入职培训形式",
        "unequal_variance_case": "客服辅助工具",
        "diagnostic_only_case": "培训方案",
        "non_significant_case": "知识检索界面",
    }
    return labels[spec.case_id]


def _seed(case_id: str) -> int:
    return {
        "clean_anova_case": 20260701,
        "unequal_variance_case": 20260702,
        "diagnostic_only_case": 20260703,
        "non_significant_case": 20260704,
    }[case_id]


def _strip_sentence_end(text: str) -> str:
    return text.rstrip("。.")
