# Quality Check

This QA report checks whether the workflow stayed inside the approved human-in-the-loop boundary, used the expected data and analysis path, and generated public-safe reporting assets.

QA is intentionally layered: hard checks cover workflow validity and public safety; soft checks cover stable machine-checkable reporting rules; editorial checks record human review items without turning every writing preference into an automated failure.

## Workflow Gate

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Human approval gate | `pass` | 3/3 outcomes include approved analysis paths. | Pause report generation and update the outcome-level human review decision file. |
| Formal outputs after approval | `pass` | Formal outputs were generated in the report stage. | Do not generate report assets until all required approvals are recorded. |
| Blocked decisions absent | `pass` | This report stage did not proceed from diagnostic_only or stop_analysis. | Stop formal reporting and return only diagnostic guidance. |

## Data & Analysis Integrity

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Outcome coverage | `pass` | Configured outcomes: 3; analyzed outcomes: 3. | Rerun analyses for missing outcomes or update the analysis plan. |
| Analysis path consistency | `pass` | Classical ANOVA maps to Tukey HSD; Welch ANOVA maps to Games-Howell. | Align the approved analysis path and post hoc method for each outcome. |
| Baseline and focal groups | `pass` | Baseline: Reading_Materials; focal: Mentor_Guided. | Set valid baseline_condition and focal_condition in analysis_plan.yaml. |
| Formal report asset completeness | `pass` | Generated final Word report, Chinese Markdown report, figure, mean table, and analysis results JSON. | Rerun the report stage and inspect the final Word report, figure, mean table, and analysis JSON. |

## Statistical Reporting Quality

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Omnibus statistics | `pass` | Each outcome includes df, statistic, p value, and effect size. | Rebuild analysis_results.json from the confirmed analysis runner. |
| APA symbols | `pass` | Markdown report includes italicized APA statistical symbols. | Regenerate result paragraphs with APA symbol formatting. |
| Percent interpretation | `pass` | Core result compares 导师带教 against 阅读材料. | Add dynamic percentage interpretation to the core results section. |
| Positive and negative direction wording | `pass` | Core percentage summary distinguishes increase and decrease wording. | Check outcome_directions in analysis_plan.yaml. |

## Report Structure & Communication

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Two-part report structure | `pass` | Report uses core content plus detailed statistical report sections. | Restore the two-part report structure. |
| Core content subsections | `pass` | Core content is split into goal, result, and recommendation subsections. | Add the three required subsections under core content. |
| Table in detailed report | `pass` | Table 1 appears under the detailed statistical report section. | Move Table 1 below the method-selection paragraph in Section 2. |
| No report-level mock data disclaimer | `warning` | Formal business report does not foreground the mock-data disclaimer. | Keep mock-data disclosure in README/privacy docs rather than the formal report body. |

## Table & Figure QA

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Figure output | `pass` | outputs/evaluation_runs/clean_anova_case/figure_combined_raincloud.png | Regenerate the combined raincloud figure. |
| Figure title above image | `pass` | Figure title is report text before the image, not embedded inside the plot. | Move the figure title above the image in Markdown and Word. |
| Table title above table | `pass` | Table title appears before the rendered mean table. | Move the table title above the table. |
| Table and figure notes | `pass` | Figure and table notes are generated as report text below the visual assets. | Regenerate notes below the corresponding figure and table. |

## Report Editorial QA

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Core result readability | `manual` | Confirm percentage interpretation is integrated into the core result paragraph rather than listed as a separate mechanical note. | Revise the report template or report_context wording, then regenerate the report. |
| Figure/table block presentation | `manual` | Review each figure/table as one block: title, visual or table body, note, and surrounding whitespace. | Adjust block spacing helpers, caption wording, figure size, or table geometry. |
| Rendered Word layout QA | `manual` | Render the DOCX and inspect for isolated headings, cramped tables, awkward page breaks, or overlapping figure annotations. | Revise Word spacing, keep-with-next behavior, figure dimensions, or table width before publishing. |

## Privacy & Public Showcase Safety

| Check | Status | Evidence | Action if Failed |
| --- | --- | --- | --- |
| Local path exposure | `pass` | No local absolute paths found in text outputs. | Replace absolute paths with project-relative paths before publishing. |
| Secret-like strings | `pass` | No API keys, tokens, passwords, or similar secret markers found. | Remove secrets and rotate any exposed credentials. |
| Personal contact leakage | `pass` | No email-like strings found in generated text outputs. | Remove personal contact information unless intentionally public. |

## Outcome Labels

- `learning_effectiveness`: 学习效果
- `onboarding_confidence`: 上手信心
- `training_burden`: 培训负担感

## Guardrail Confirmation

- No formal APA-style results, table, figure, or Word report should be generated before approval.
- This run used the explicit outcome-level approval recorded in `config/human_review_decision.yaml`.
- `diagnostic_only` and `stop_analysis` are not present in this run.
