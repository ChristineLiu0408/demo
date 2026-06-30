"""Tests for report helper behavior."""

from __future__ import annotations

from copy import deepcopy

import pytest

from src.analysis_runner import run_confirmed_analyses
from src.quality_check import run_quality_check
from src.report_writer import _percent_change, render_report_markdown
from src.table_generator import build_mean_table, compact_letter_display
from src.utils import load_yaml, write_text


TEST_DECISION = "config/human_review_decision.test.yaml"


def _run_test_analyses():
    return run_confirmed_analyses(decision_path=TEST_DECISION)


def test_percent_change_uses_no_ai_baseline():
    plan = load_yaml("config/analysis_plan.yaml")
    results = _run_test_analyses()

    assert round(_percent_change("task_efficiency", results["outcomes"]["task_efficiency"], plan), 1) == pytest.approx(40.7)
    assert round(_percent_change("work_confidence", results["outcomes"]["work_confidence"], plan), 1) == pytest.approx(40.6)
    assert round(_percent_change("perceived_workload", results["outcomes"]["perceived_workload"], plan), 1) == pytest.approx(28.3)


def test_report_uses_revised_two_part_structure():
    plan = load_yaml("config/analysis_plan.yaml")
    results = _run_test_analyses()
    table = build_mean_table(results, plan)
    text = render_report_markdown(results, plan, table, "outputs/figure_combined_raincloud.png")

    assert "## 1. 核心内容" in text
    assert "### 1.1 报告目标" in text
    assert "### 1.2 核心结果" in text
    assert "### 1.3 行动建议" in text
    assert "## 2. 详细统计报告" in text
    assert "synthetic/mock data" not in text
    assert "智能体AI辅助相较无AI辅助" in text
    assert "\n其中，智能体AI辅助相较无AI辅助" not in text
    assert "降低得越低。其中，智能体AI辅助相较无AI辅助" in text
    assert "### 1.3 核心趋势图" not in text


def test_figure_and_table_titles_are_above_assets():
    plan = load_yaml("config/analysis_plan.yaml")
    results = _run_test_analyses()
    table = build_mean_table(results, plan)
    text = render_report_markdown(results, plan, table, "outputs/figure_combined_raincloud.png")

    assert "**图 1. 不同AI辅助工具的效果**" in text
    assert text.index("**图 1.") < text.index("![图 1]")
    assert text.index("**表 1.") < text.index("结果指标", text.index("**表 1."))
    assert text.index("## 2. 详细统计报告") < text.index("**表 1.")
    assert text.index("![图 1]") < text.index("注：点表示个体观测值")
    assert text.index("结果指标", text.index("**表 1.")) < text.index("注：数值为均值")


def test_report_template_can_use_non_ai_context():
    plan = deepcopy(load_yaml("config/analysis_plan.yaml"))
    plan["reporting"]["analysis_title"] = "培训方案效果评估报告"
    plan["analysis"]["grouping_variable_label_zh"] = "培训条件"
    plan["analysis"]["condition_labels_zh"] = {
        "No_AI_Support": "对照组",
        "Basic_Chatbot": "基础培训",
        "Workflow_Assistant": "强化培训",
        "Agentic_Assistant": "综合培训",
    }
    plan["analysis"]["outcome_labels_zh"] = {
        "task_efficiency": "任务表现",
        "work_confidence": "学习信心",
        "perceived_workload": "认知负荷",
    }
    plan["reporting"]["report_context"] = {
        "participant_label": "参与者",
        "overview_sentence": "本次评估比较了{group_labels}在{outcome_list}上的差异，以支持{decision_context}。",
        "questions": ["不同培训条件是否影响结果指标？", "哪个培训条件对应更理想的结果模式？"],
        "core_findings": ["第一，不同培训条件之间存在清晰差异。", "第二，整体结果支持继续优化培训方案。"],
        "implication_sentence": "上述结果趋势见图1。",
        "action_recommendations": ["后续可以优先验证表现较好的培训条件。"],
    }
    results = _run_test_analyses()
    table = build_mean_table(results, plan)
    text = render_report_markdown(results, plan, table, "outputs/figure_combined_raincloud.png")

    assert "AI辅助" not in text
    assert "培训条件" in text
    assert "综合培训相较对照组" in text


def test_quality_check_uses_six_modules():
    plan = load_yaml("config/analysis_plan.yaml")
    results = _run_test_analyses()
    table = build_mean_table(results, plan)
    markdown_path = write_text(
        "outputs/business_friendly_report_zh.md",
        render_report_markdown(results, plan, table, "outputs/figure_combined_raincloud.png"),
    )
    generated_files = {
        "analysis_results": write_text("outputs/analysis_results.json", "{}\n"),
        "mean_table": write_text("outputs/mean_table_compact_letters.csv", table.to_csv(index=False)),
        "figure": "outputs/figure_combined_raincloud.png",
        "markdown_report": markdown_path,
        "word_report": "outputs/final_report.docx",
    }

    quality_path = run_quality_check(results, plan, generated_files)
    quality_text = quality_path.read_text(encoding="utf-8")

    for heading in [
        "## Workflow Gate",
        "## Data & Analysis Integrity",
        "## Statistical Reporting Quality",
        "## Report Structure & Communication",
        "## Table & Figure QA",
        "## Report Editorial QA",
        "## Privacy & Public Showcase Safety",
    ]:
        assert heading in quality_text
    assert "QA is intentionally layered" in quality_text
    assert "| Core result readability | `manual` |" in quality_text
    assert "Formal report asset completeness" in quality_text
    assert "| Check | Status | Evidence | Action if Failed |" in quality_text


def test_compact_letters_keep_all_significant_groups_separate():
    groups = ["No_AI_Support", "Basic_Chatbot", "Workflow_Assistant", "Agentic_Assistant"]
    pairwise = [
        {"group_a": a, "group_b": b, "significant": True, "p_adj": 0.001}
        for i, a in enumerate(groups)
        for b in groups[i + 1 :]
    ]

    letters = compact_letter_display(groups, pairwise)

    assert len(set(letters.values())) == 4
