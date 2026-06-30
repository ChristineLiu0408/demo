# Human Review Required

The suitability check has finished. The workflow is intentionally paused before formal statistical reporting.

- Overall recommendation: `diagnostic_only`
- Approval file required: `scenarios/diagnostic_only_case/human_review_decision.yaml`

## Outcome-Level Recommendations

| Outcome | Decision | Analysis path | Post hoc |
| --- | --- | --- | --- |
| `knowledge_mastery` | `diagnostic_only` | `none` | `none` |
| `transfer_confidence` | `diagnostic_only` | `none` | `none` |
| `training_fatigue` | `diagnostic_only` | `none` | `none` |

## Required Human Action

Review `outputs/anova_suitability_check.md`. If the recommended path is appropriate, create `config/human_review_decision.yaml` from `config/human_review_decision.example.yaml` and set:

```yaml
approval_status: approved
approved_analysis_path: classical_anova
```

Use `approved_analysis_path: welch_anova` if the reviewed recommendation is Welch ANOVA.

If the decision is `diagnostic_only` or `stop_analysis`, do not approve formal report generation without revising the data, analysis plan, or MVP scope.

Until approval is present, the workflow must not generate APA result paragraphs, formal statistical tables, result figures, or Word reports.
