# AI Statistical Reporting Workflow Demo

This repository is a public showcase MVP for a human-in-the-loop AI statistical reporting workflow.

## 面试官快速入口

如果你只想快速了解项目，请按顺序查看：

1. [重点展示材料/00_先看这里_项目导览.md](重点展示材料/00_先看这里_项目导览.md)
2. [重点展示材料/01_最终报告样例_人工智能辅助试点.docx](重点展示材料/01_最终报告样例_人工智能辅助试点.docx)
3. [重点展示材料/02_workflow可视化总览.png](重点展示材料/02_workflow可视化总览.png)
4. [重点展示材料/03_稳定性评估可视化.png](重点展示材料/03_稳定性评估可视化.png)
5. [重点展示材料/04_稳定性评估报告.md](重点展示材料/04_稳定性评估报告.md)
6. [重点展示材料/06_质量检查报告.md](重点展示材料/06_质量检查报告.md)
7. [重点展示材料/07_方差分析适用性检查.md](重点展示材料/07_方差分析适用性检查.md)

这个项目是 portfolio demo / workflow prototype，所有数据和场景均为 synthetic/mock data，不代表真实业务证据或真实研究结果。

The demo is designed for social science researchers who have a structured dataset and an analysis plan, and who want support with repetitive reporting work: data checks, ANOVA suitability diagnostics, statistical analysis, APA-style results writing, tables, figures, Word export, and quality checks.

## Why Pure Python

This MVP uses a pure Python implementation to reduce local setup friction for GitHub reviewers, interviewers, and non-specialist users.

The first version only supports a controlled one-way ANOVA workflow, so Python is sufficient for:

- data processing with `pandas` and `numpy`
- assumption checks with `scipy`
- classical one-way ANOVA and Tukey HSD with `statsmodels`
- Welch ANOVA and Games-Howell post hoc tests with `pingouin`
- result figures with `matplotlib`
- Word report export with `python-docx`
- YAML configuration with `pyyaml`
- basic regression tests with `pytest`

For more complex social science analyses, later versions may consider R or professional statistical software integration. The first MVP intentionally focuses on a lightweight, reproducible one-way ANOVA workflow.

## MVP Scenario

The mock scenario is a synthetic workplace AI productivity study.

Example research question:

> Does AI support condition influence employee task efficiency, work confidence, or perceived workload?

The demo uses only synthetic data. It does not include real manuscripts, real research data, unpublished findings, collaborator information, local paths, API keys, or private Codex Skill source text.

## Human-in-the-Loop Workflow

1. User provides `data/employee_ai_support_mock.csv`.
2. User provides `config/analysis_plan.yaml`.
3. The workflow runs an ANOVA suitability check.
4. The workflow writes `outputs/anova_suitability_check.md`.
5. The workflow writes `outputs/human_review_required.md`.
6. The workflow stops before formal statistical conclusions are generated.
7. User reviews the recommendation and creates `config/human_review_decision.yaml`.
8. If `approval_status: approved`, the workflow runs the confirmed analysis path.
9. The workflow generates APA-style results, tables, figures, a Word report, and `quality_check.md`.

## Statistical Decision Guardrail

The suitability check is not a simple pass/fail validator. It is a reproducible statistical decision guardrail that checks data structure, data quality, and one-way ANOVA assumptions before any formal reporting output is created.

The guardrail can return four decisions:

- `classical_anova_recommended`: ordinary one-way ANOVA is eligible; post hoc path is Tukey HSD.
- `welch_anova_recommended`: variance homogeneity is not met or is uncertain; post hoc path is Games-Howell.
- `diagnostic_only`: the data structure is basically readable, but risk is too high for automatic formal conclusions.
- `stop_analysis`: the analysis plan or data structure is outside the one-way ANOVA MVP.

The ordinary ANOVA vs Welch ANOVA switch is mainly driven by variance homogeneity:

- Levene's test p >= .05 and max/min variance ratio <= 2: classical ANOVA is eligible.
- Levene's test p < .05 or max/min variance ratio > 2: Welch ANOVA is recommended.
- Levene's test p < .01 and max/min variance ratio > 4: strong warning; if combined with small samples, severe imbalance, or severe outliers, the workflow switches to `diagnostic_only`.

Normality warnings, mild missingness, and mild outlier flags are reported for human review, but they do not automatically force Welch ANOVA. The workflow is designed to support researcher judgment, not replace it.

## Run the Suitability Check

```bash
pip install -r requirements.txt
python -m src.workflow --stage check
```

The check stage writes:

- `outputs/anova_suitability_check.md`
- `outputs/human_review_required.md`

It does not generate APA result paragraphs, formal statistical tables, result figures, or Word reports before human approval.

## Implemented Outputs

After human approval, the MVP generates:

- `outputs/analysis_results.json`: machine-readable ANOVA results and descriptives
- `outputs/mean_table_compact_letters.csv`: APA-style compact-letter mean table
- `outputs/figure_combined_raincloud.png`: manuscript-ready combined raincloud figure
- `outputs/business_friendly_report_zh.md`: business-friendly Chinese statistical report
- `outputs/final_report.docx`: Word report containing the narrative, table, figure, and notes
- `outputs/quality_check.md`: layered workflow, statistical, reporting, editorial, and privacy QA report

The MVP intentionally does not generate a separate full post-hoc comparison table in v1. Post-hoc results are used to create compact letter displays, significance brackets, and result paragraphs.

## Evaluation Layer

The repository includes a lightweight evaluation layer with four synthetic business scenarios:

- `clean_anova_case`: ordinary ANOVA path.
- `unequal_variance_case`: Welch ANOVA path.
- `diagnostic_only_case`: guardrail blocks formal reporting.
- `non_significant_case`: report remains restrained when group differences are not stable.

Run the evaluation with:

```bash
python -m src.evaluation_runner
```

The evaluation writes `docs/evaluation_report.md` and per-case outputs under `outputs/evaluation_runs/`. These cases are for workflow stability and public showcase only; they do not claim coverage of all statistical analyses.

For the three cases that are eligible for formal reporting, the evaluation runner writes `final_report.docx` files for manual review. These reports support the current confirmed metrics for Human Edit Rate, Statistical Claim Traceability Rate, and Time Saved. The `diagnostic_only_case` should remain blocked and should not generate a formal Word report.

## Project Structure

```text
ai-stat-report-workflow-demo/
├── README.md
├── privacy_audit.md
├── requirements.txt
├── data/
├── config/
├── scenarios/
├── src/
├── prompts/
├── outputs/
├── docs/
├── screenshots/
└── tests/
```

## MVP Boundary

Included in v1:

- one-way ANOVA workflow only
- synthetic workplace AI support dataset
- suitability check before analysis
- explicit human approval gate
- classical ANOVA or Welch ANOVA path
- Tukey HSD or Games-Howell post hoc path
- APA-style reporting assets

Deferred to later versions:

- repeated-measures ANOVA
- factorial ANOVA
- ANCOVA
- regression and mediation models
- mixed-effects models
- R integration
- LLM API orchestration
- web UI
- multi-agent workflow execution

## Status

This repository currently includes the synthetic dataset, public documentation, YAML decision rules, suitability-check guardrail, human approval gate, confirmed analysis runner, business-friendly report generation, APA-style mean table, combined figure, Word export, and layered quality check. Formal statistical outputs are generated only after the human approval file is present.
