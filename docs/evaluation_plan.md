# Evaluation Plan

## Evaluation Goals

The demo should be evaluated as an AI workflow product, not only as a statistical script.

Key questions:

- Does the workflow stop at the right decision point?
- Are the generated outputs consistent with the approved analysis path?
- Can a reviewer reproduce the results locally?
- Does the documentation explain the product value clearly?

The current lightweight stability evaluation is implemented through four synthetic scenarios under `scenarios/`. Run `python -m src.evaluation_runner` to regenerate `docs/evaluation_report.md`.

For cases that pass the guardrail and include the prefilled evaluation approval fixture, the runner also generates per-case Word reports under `outputs/evaluation_runs/`. These Word reports are the manual review materials for estimating Human Edit Rate, Error Detection Rate, and Time Saved. The `diagnostic_only_case` should not produce a formal Word report.

## Functional Evaluation

- Verify that the workflow loads the mock dataset and analysis plan.
- Verify that missing required columns are detected.
- Verify that suitability reports are generated before formal analysis.
- Verify that formal outputs are blocked until approval.
- Verify that approved classical ANOVA and Welch ANOVA paths are handled.
- Verify that `diagnostic_only` and `stop_analysis` decisions do not generate formal APA paragraphs, formal tables, figures, or Word reports.

## Guardrail Evaluation

- Confirm that `classical_anova_recommended` is returned when structure, missingness, sample size, outliers, normality risk, and variance homogeneity are acceptable.
- Confirm that `welch_anova_recommended` is returned when variance homogeneity is not met but other risks remain acceptable.
- Confirm that `diagnostic_only` is returned for severe missingness, severe outliers, severe small-sample nonnormality, or extreme heterogeneity combined with additional risk.
- Confirm that `stop_analysis` is returned for structural incompatibilities such as missing grouping variables, fewer than two groups, nonnumeric dependent variables, duplicate participant IDs across groups, or repeated/nested design hints.
- Confirm that each report includes check-level status, key statistics, interpretation, and recommended path.

## Statistical Consistency Evaluation

- Check that the selected post-hoc method matches the approved analysis path.
- Check that p-values, degrees of freedom, and effect-size labels are consistent across outputs.
- Check that table values match the analysis runner output.
- Check that figure labels match the analysis plan.

## Quality Check Evaluation

The quality check is intentionally layered so the workflow does not turn every writing preference into a brittle automated rule.

### Hard QA

Hard QA covers workflow validity and public-safety risks. Failures should block publication or require immediate correction.

- Confirm that formal outputs are generated only after human approval.
- Confirm that `diagnostic_only` and `stop_analysis` decisions do not generate formal reports.
- Confirm that all configured outcomes are analyzed.
- Confirm that the selected ANOVA path and post-hoc method are consistent.
- Confirm that generated public outputs do not expose local paths, secrets, real data, or private research materials.

### Soft QA

Soft QA covers stable machine-checkable reporting rules. Failures can be shown as warnings when they do not invalidate the workflow.

- Confirm that the report contains the required two-part structure.
- Confirm that the compact-letter mean table appears under the detailed statistical report.
- Confirm that figure and table titles appear above their visual assets.
- Confirm that figure and table notes are present below their assets.
- Confirm that the report includes baseline-relative percentage interpretation.

### Editorial QA

Editorial QA covers writing and Word layout quality. These checks are recorded as manual review items rather than automatic pass/fail rules.

- Render the Word report and inspect for isolated headings, cramped tables, awkward page breaks, or overlapping figure annotations.
- Review whether the core results read naturally and do not mechanically list percentages.
- Review whether each figure/table block reads as a coherent unit: title, visual or table body, note, and surrounding whitespace.

## Human-in-the-Loop Evaluation

- Confirm that `human_review_required.md` clearly explains what the reviewer must inspect.
- Confirm that `human_review_decision.yaml` is required before formal reporting.
- Confirm that the workflow records the approved analysis path.
- Confirm that generated evaluation-case Word reports are treated as pending manual review materials, not as already human-approved final business evidence.

## Manual Review Evaluation

The following metrics require human review and should not be claimed as fully measured until the generated Word reports are inspected:

- Human Edit Rate: proportion of generated content requiring manual edits in wording, statistics, table/figure presentation, or layout.
- Error Detection Rate: number and type of issues prevented by guardrails or found during manual review.
- Time Saved: estimated time difference between manual report creation and workflow-assisted creation, recorded as a practical estimate rather than an experimental baseline unless a baseline study is conducted.

## Public Showcase Evaluation

- README explains the workflow in plain language.
- No private data, real manuscript content, or original private Skill text is included.
- Screenshots show only synthetic data and public-safe outputs.
- The project can be understood as an MVP for AI workflow automation and reporting quality control.
