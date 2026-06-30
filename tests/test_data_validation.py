"""Tests for data validation behavior."""

from __future__ import annotations

import pandas as pd

from src.data_validation import participant_id_issue, repeated_or_nested_hint_columns


def test_duplicate_participant_across_groups_is_flagged():
    df = pd.DataFrame(
        {
            "participant_id": ["P001", "P001"],
            "ai_support_condition": ["No_AI_Support", "Basic_Chatbot"],
            "score": [3.0, 4.0],
        }
    )

    assert participant_id_issue(df, "ai_support_condition") == "duplicated_participant_id_across_groups"


def test_nested_hint_column_is_detected():
    df = pd.DataFrame({"participant_id": ["P001"], "team_id": ["T01"], "score": [3.0]})

    assert repeated_or_nested_hint_columns(df) == ["team_id"]
