"""Tests for synthetic evaluation scenarios."""

from __future__ import annotations

import pytest

from src.evaluation_cases import SCENARIOS, ensure_evaluation_scenarios
from src.evaluation_runner import run_evaluation
from src.suitability_check import run_suitability_check
from src.workflow import run_report_stage


def test_evaluation_scenarios_have_expected_decisions(tmp_path):
    ensure_evaluation_scenarios()
    expected = {
        "clean_anova_case": "classical_anova_recommended",
        "unequal_variance_case": "welch_anova_recommended",
        "diagnostic_only_case": "diagnostic_only",
        "non_significant_case": "classical_anova_recommended",
    }

    for case_id, decision in expected.items():
        result = run_suitability_check(
            analysis_plan_path=f"scenarios/{case_id}/analysis_plan.yaml",
            output_dir=tmp_path / case_id,
        )
        assert result["overall_decision"] == decision


def test_diagnostic_only_case_blocks_formal_report(tmp_path):
    ensure_evaluation_scenarios()
    with pytest.raises(RuntimeError, match="diagnostic_only"):
        run_report_stage(
            analysis_plan_path="scenarios/diagnostic_only_case/analysis_plan.yaml",
            decision_path="scenarios/diagnostic_only_case/human_review_decision.yaml",
            output_dir=tmp_path / "diagnostic_only_case",
        )

    assert not (tmp_path / "diagnostic_only_case" / "final_report.docx").exists()


def test_non_significant_case_uses_restrained_wording(tmp_path):
    ensure_evaluation_scenarios()
    run_report_stage(
        analysis_plan_path="scenarios/non_significant_case/analysis_plan.yaml",
        decision_path="scenarios/non_significant_case/human_review_decision.yaml",
        output_dir=tmp_path / "non_significant_case",
    )
    report = (tmp_path / "non_significant_case" / "business_friendly_report_zh.md").read_text(encoding="utf-8")

    assert "未发现稳定组间差异" in report
    assert "不应将该均值差异解读为明确业务效果" in report
    assert "影响显著" not in report
    assert "明显差异" not in report
    assert "明显优于" not in report
    assert "*ps* < .05" not in report


def test_evaluation_report_summarizes_four_cases(tmp_path):
    report_path = run_evaluation(
        output_dir=tmp_path / "evaluation_runs",
        report_path=tmp_path / "evaluation_report.md",
    )
    report = report_path.read_text(encoding="utf-8")

    assert "任务完成率 | 4/4" in report
    assert "决策路径准确率 | 4/4" in report
    assert "人工确认合规率 | 4/4" in report
    assert "报告完整率 | 4/4" in report
    assert "文本、表格、图表一致率 | 4/4" in report
    assert "统计格式通过率 | 4/4" in report
    assert "人工审核修改率" in report
    assert "8.52%" in report
    assert "407" in report
    assert "4,776" in report
    assert "统计结论可追溯率" in report
    assert "100%" in report
    assert "10 分钟" in report
    assert "90 分钟" in report
    assert "88.9%" in report
    assert "约九倍" in report
    assert "已为可报告情景生成待人工复核的文档报告" in report
    assert "预填人工确认文件" in report
    assert "Error Detection Rate" not in report
    assert "Manual Edit Notes" not in report
    assert "错误检出率" not in report
    assert "人工备注" not in report
    for case_id in SCENARIOS:
        assert f"{case_id}" not in report
    assert "不报告错误降低率百分比" in report
