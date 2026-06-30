"""Data validation utilities for the one-way ANOVA MVP."""

from __future__ import annotations

import pandas as pd


REPEATED_OR_CLUSTER_HINT_COLUMNS = {
    "time",
    "timepoint",
    "wave",
    "session",
    "trial",
    "round",
    "cluster",
    "cluster_id",
    "team_id",
    "department_id",
    "manager_id",
    "classroom_id",
    "school_id",
}


def participant_id_issue(df: pd.DataFrame, grouping_variable: str) -> str | None:
    if "participant_id" not in df.columns:
        return None
    duplicate_ids = df[df["participant_id"].duplicated(keep=False)]
    if duplicate_ids.empty:
        return None
    group_counts = duplicate_ids.groupby("participant_id")[grouping_variable].nunique()
    if (group_counts > 1).any():
        return "duplicated_participant_id_across_groups"
    return "duplicated_participant_id_records"


def repeated_or_nested_hint_columns(df: pd.DataFrame) -> list[str]:
    normalized = {column.lower(): column for column in df.columns}
    return [
        original
        for lowered, original in normalized.items()
        if lowered in REPEATED_OR_CLUSTER_HINT_COLUMNS
    ]
