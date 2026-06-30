# Product Requirements Document

## Product Name

AI Statistical Reporting Workflow Demo

## Positioning

This project demonstrates a human-in-the-loop AI workflow for statistical reporting in social science research. It focuses on a narrow but realistic MVP: one-way ANOVA reporting from a structured mock dataset and a YAML analysis plan.

The goal is to show workflow design ability, not to replace statistical judgment.

The first implemented module is a statistical decision guardrail. It automates reproducible checks and recommends an analysis path, while keeping the final statistical decision with a human reviewer.

## Target Users

- social science researchers
- graduate students preparing manuscript results sections
- research assistants who repeatedly transform statistical outputs into reports, tables, and figures

## User Problem

Researchers often repeat the same workflow:

1. check whether the planned analysis is appropriate
2. run the statistical test
3. format results in APA style
4. create tables and figures
5. check that text, tables, figures, and statistics agree
6. export a document for review

This process is time-consuming and error-prone, especially when values are copied across multiple outputs.

## MVP Goal

Build a pure Python, local-first workflow that:

- accepts a synthetic CSV dataset
- accepts a YAML analysis plan
- checks whether one-way ANOVA is suitable
- pauses for human review before formal analysis
- runs approved one-way ANOVA or Welch ANOVA
- generates APA-style results, a compact-letter mean table, a combined figure, Word output, and a quality check

## Non-Goals

- support all statistical models
- automate scientific judgment
- publish real research data
- expose private Codex Skill source text
- build a web application in v1
- depend on R in v1

## Functional Requirements

- FR1: Load `data/employee_ai_support_mock.csv`.
- FR2: Load `config/analysis_plan.yaml`.
- FR3: Validate required columns and variable types.
- FR4: Run assumption and suitability checks defined in `config/statistical_decision_rules.yaml`.
- FR5: Generate `outputs/anova_suitability_check.md`.
- FR6: Generate `outputs/human_review_required.md`.
- FR7: Stop before analysis unless `config/human_review_decision.yaml` approves the analysis path.
- FR8: Run classical ANOVA or Welch ANOVA after approval.
- FR9: Generate an APA-style compact-letter mean table; use post-hoc results for compact letters, figure brackets, and result paragraphs.
- FR10: Generate a combined matplotlib figure for all configured outcomes.
- FR11: Generate a Word report with business-friendly result paragraphs, the mean table, figure, and notes.
- FR12: Generate `outputs/quality_check.md`.

## Guardrail Decision Logic

The suitability module returns one of four decisions:

- `classical_anova_recommended`: data structure is valid, missingness and sample sizes are acceptable, no severe outlier or small-sample normality issue is detected, and variance homogeneity is acceptable. The recommended path is ordinary one-way ANOVA plus Tukey HSD.
- `welch_anova_recommended`: data structure and quality checks are acceptable, but variance homogeneity is not met or is uncertain. The recommended path is Welch ANOVA plus Games-Howell post hoc tests.
- `diagnostic_only`: data can be read, but risk is too high for automatic formal conclusions, such as severe missingness, severe outlier concentration, small-sample nonnormality, or extreme heterogeneity combined with other risks.
- `stop_analysis`: the analysis plan is structurally incompatible with the one-way ANOVA MVP, such as missing grouping variables, fewer than two groups, missing or nonnumeric dependent variables, duplicate participant IDs across groups, or repeated/nested design hints.

## Product Guardrail Requirement

The workflow must not create formal APA results, formal statistical tables, figures, or Word reports before human approval. The value proposition is AI-assisted reproducibility and workflow efficiency, not unsupervised statistical decision-making.

## Success Metrics

- A reviewer can understand the workflow from README and docs in under five minutes.
- A reviewer can run the MVP locally with standard Python dependencies.
- The workflow does not generate formal conclusions before human approval.
- The suitability report shows check-level statuses, key statistics, and recommended analysis paths.
- Generated text, tables, and figures use the same statistical values.
- The public repository contains only synthetic data and reviewed sample outputs.
