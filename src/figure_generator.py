"""Matplotlib figure generation utilities for result visualizations."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".mplconfig"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from scipy.stats import gaussian_kde

from .utils import project_path


COLORS = {
    "No_AI_Support": "#4C78A8",
    "Basic_Chatbot": "#59A14F",
    "Workflow_Assistant": "#E15759",
    "Agentic_Assistant": "#B07AA1",
}
DEFAULT_PALETTE = ["#4C78A8", "#59A14F", "#E15759", "#B07AA1", "#F28E2B", "#76B7B2"]


def create_combined_raincloud_figure(
    data: pd.DataFrame,
    results: dict[str, Any],
    plan: dict[str, Any],
    output_path: str | Path = "outputs/figure_combined_raincloud.png",
) -> Path:
    _setup_fonts()
    grouping = plan["analysis"]["grouping_variable"]
    group_order = plan["analysis"]["condition_order"]
    group_labels = plan["analysis"]["condition_labels_zh"]
    outcome_labels = plan["analysis"]["outcome_labels_zh"]
    outcomes = plan["analysis"]["outcome_variables"]

    fig, axes = plt.subplots(1, len(outcomes), figsize=(13.2, 4.5), sharey=True)
    rng = np.random.default_rng(20260627)
    for ax, outcome in zip(axes, outcomes):
        _draw_panel(ax, data, results["outcomes"][outcome], grouping, outcome, group_order, group_labels, rng)
        ax.set_title(outcome_labels[outcome], fontsize=12, fontweight="bold", pad=10)
        ax.set_xticks(range(1, len(group_order) + 1))
        ax.set_xticklabels([group_labels[group] for group in group_order], fontsize=8)
        ax.set_ylim(1, 8.35)
        ax.set_yticks(range(1, 8))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", color="#E5E5E5", linewidth=0.6)
    axes[0].set_ylabel("评分", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 1), w_pad=1.6)
    path = project_path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def _draw_panel(
    ax: plt.Axes,
    data: pd.DataFrame,
    outcome_result: dict[str, Any],
    grouping: str,
    outcome: str,
    group_order: list[str],
    group_labels: dict[str, str],
    rng: np.random.Generator,
) -> None:
    for idx, group in enumerate(group_order, start=1):
        values = data.loc[data[grouping] == group, outcome].dropna().astype(float).to_numpy()
        color = _group_color(group, idx)
        _half_violin(ax, values, idx, color)
        jitter = rng.uniform(-0.33, -0.20, size=len(values))
        ax.scatter(np.full(len(values), idx) + jitter, values, s=12, alpha=0.58, color=color, edgecolor="white", linewidth=0.25, zorder=3)
        ax.boxplot(
            values,
            positions=[idx],
            widths=0.18,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "black", "linewidth": 1.2},
            boxprops={"facecolor": "white", "edgecolor": "black", "linewidth": 1.0},
            whiskerprops={"color": "black", "linewidth": 0.9},
            capprops={"color": "black", "linewidth": 0.9},
        )
    _add_significance_brackets(ax, outcome_result["pairwise"], group_order)


def _half_violin(ax: plt.Axes, values: np.ndarray, x: float, color: str) -> None:
    if len(values) < 3 or np.std(values) == 0:
        return
    y = np.linspace(1, 7, 200)
    density = gaussian_kde(values)(y)
    density = density / density.max() * 0.32
    ax.fill_betweenx(y, x, x + density, color=color, alpha=0.65, linewidth=0)


def _add_significance_brackets(ax: plt.Axes, pairwise: list[dict[str, Any]], group_order: list[str]) -> None:
    height_by_pair = {
        frozenset([group_order[0], group_order[1]]): 7.22,
        frozenset([group_order[1], group_order[2]]): 7.22,
        frozenset([group_order[2], group_order[3]]): 7.22,
        frozenset([group_order[0], group_order[2]]): 7.48,
        frozenset([group_order[0], group_order[3]]): 7.74,
        frozenset([group_order[1], group_order[3]]): 8.00,
    }
    significant = sorted(
        [item for item in pairwise if item.get("significant")],
        key=lambda item: height_by_pair.get(frozenset([item["group_a"], item["group_b"]]), 8.20),
    )
    for item in significant:
        x1 = group_order.index(item["group_a"]) + 1
        x2 = group_order.index(item["group_b"]) + 1
        if x1 > x2:
            x1, x2 = x2, x1
        y = height_by_pair.get(frozenset([item["group_a"], item["group_b"]]), 8.20)
        h = 0.055
        ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color="black", linewidth=0.8, clip_on=False)
        ax.text((x1 + x2) / 2, y + h + 0.035, _stars(item["p_adj"]), ha="center", va="bottom", fontsize=8)


def _stars(p: float) -> str:
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"


def _group_color(group: str, index: int) -> str:
    return COLORS.get(group, DEFAULT_PALETTE[(index - 1) % len(DEFAULT_PALETTE)])


def _setup_fonts() -> None:
    for font_path in [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ]:
        if Path(font_path).exists():
            font_manager.fontManager.addfont(font_path)
    plt.rcParams["font.family"] = ["Songti SC", "Times New Roman", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
