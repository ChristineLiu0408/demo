"""APA-style summary table and compact-letter table generation utilities."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd

from .utils import project_path


LETTERS = "abcdefghijklmnopqrstuvwxyz"


def build_mean_table(results: dict[str, Any], plan: dict[str, Any]) -> pd.DataFrame:
    group_order = plan["analysis"]["condition_order"]
    group_labels = plan["analysis"]["condition_labels_zh"]
    outcome_labels = plan["analysis"]["outcome_labels_zh"]

    rows = []
    for outcome, outcome_result in results["outcomes"].items():
        letters = compact_letter_display(group_order, outcome_result["pairwise"])
        row = {"结果指标": outcome_labels.get(outcome, outcome)}
        for group in group_order:
            desc = outcome_result["descriptives"][group]
            label = group_labels.get(group, group)
            row[label] = f"{desc['mean']:.2f}{letters[group]} ({desc['sd']:.2f})"
        rows.append(row)
    return pd.DataFrame(rows)


def write_mean_table_csv(table: pd.DataFrame, path: str | Path = "outputs/mean_table_compact_letters.csv") -> Path:
    output_path = project_path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_path, index=False)
    return output_path


def compact_letter_display(group_order: list[str], pairwise: list[dict[str, Any]], alpha: float = 0.05) -> dict[str, str]:
    """Create compact letter displays for small one-way ANOVA tables.

    Groups that are significantly different should not share a letter. Groups
    that are not significantly different may share a letter when possible.
    """
    sig_pairs = {
        frozenset([item["group_a"], item["group_b"]])
        for item in pairwise
        if item.get("significant") or item.get("p_adj", 1.0) < alpha
    }
    if not sig_pairs:
        return {group: "a" for group in group_order}

    all_cliques: list[set[str]] = []
    for size in range(len(group_order), 0, -1):
        for combo in combinations(group_order, size):
            combo_set = set(combo)
            if _is_nonsignificant_clique(combo_set, sig_pairs):
                if not any(combo_set < existing for existing in all_cliques):
                    all_cliques.append(combo_set)

    assigned: dict[str, list[str]] = {group: [] for group in group_order}
    used_cliques: list[set[str]] = []
    for clique in all_cliques:
        if all(assigned[group] for group in clique):
            continue
        letter = LETTERS[len(used_cliques)]
        used_cliques.append(clique)
        for group in clique:
            assigned[group].append(letter)

    for group in group_order:
        if not assigned[group]:
            letter = LETTERS[len(used_cliques)]
            used_cliques.append({group})
            assigned[group].append(letter)

    # Remove accidental shared letters for significant pairs.
    for pair in sig_pairs:
        a, b = tuple(pair)
        shared = set(assigned[a]) & set(assigned[b])
        for letter in shared:
            assigned[b].remove(letter)
        if not assigned[b]:
            assigned[b].append(LETTERS[len(used_cliques)])
            used_cliques.append({b})

    return {group: "".join(assigned[group]) for group in group_order}


def _is_nonsignificant_clique(groups: set[str], sig_pairs: set[frozenset[str]]) -> bool:
    for a, b in combinations(groups, 2):
        if frozenset([a, b]) in sig_pairs:
            return False
    return True
