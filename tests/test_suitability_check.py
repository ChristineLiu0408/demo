"""Tests for ANOVA suitability guardrail behavior."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.suitability_check import evaluate_outcome, structural_checks
from src.utils import load_yaml


def _rules():
    return load_yaml("config/statistical_decision_rules.yaml")


def _plan(outcomes=None):
    return {
        "analysis": {
            "analysis_type": "one_way_anova",
            "grouping_variable": "ai_support_condition",
            "outcome_variables": outcomes or ["score"],
        }
    }


def test_clean_mock_dataset_recommends_classical_anova():
    df = pd.read_csv("data/employee_ai_support_mock.csv")
    rules = _rules()

    structural = structural_checks(df, _plan(["task_efficiency"]), rules)
    outcome = evaluate_outcome(df, "ai_support_condition", "task_efficiency", rules)

    assert all(check.status != "stop_analysis" for check in structural)
    assert outcome.decision == "classical_anova_recommended"
    assert outcome.recommended_posthoc == "tukey_hsd"


def test_variance_heterogeneity_recommends_welch_anova():
    rng = np.random.default_rng(42)
    rows = []
    specs = [
        ("No_AI_Support", 4.0, 0.45),
        ("Basic_Chatbot", 4.3, 0.45),
        ("Workflow_Assistant", 4.6, 0.45),
        ("Agentic_Assistant", 4.9, 1.35),
    ]
    for group, mean, sd in specs:
        values = rng.normal(mean, sd, 30)
        for value in values:
            rows.append({"participant_id": f"P{len(rows) + 1:03d}", "ai_support_condition": group, "score": value})
    df = pd.DataFrame(rows)

    outcome = evaluate_outcome(df, "ai_support_condition", "score", _rules())

    assert outcome.decision == "welch_anova_recommended"
    assert outcome.recommended_posthoc == "games_howell"


def test_missing_grouping_variable_stops_analysis():
    df = pd.DataFrame({"participant_id": ["P001", "P002"], "score": [3.0, 4.0]})

    checks = structural_checks(df, _plan(), _rules())

    assert any(check.name == "grouping_variable_present" and check.status == "stop_analysis" for check in checks)
