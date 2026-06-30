# Human Review Required

The suitability check has finished. The workflow is intentionally paused before formal statistical reporting.

- Overall recommendation: `welch_anova_recommended`
- Approval file required: `scenarios/unequal_variance_case/human_review_decision.yaml`

## Outcome-Level Recommendations

| Outcome | Decision | Analysis path | Post hoc |
| --- | --- | --- | --- |
| `resolution_efficiency` | `welch_anova_recommended` | `welch_anova` | `games_howell` |
| `service_confidence` | `welch_anova_recommended` | `welch_anova` | `games_howell` |
| `cognitive_load` | `welch_anova_recommended` | `welch_anova` | `games_howell` |

## Required Human Action

Review `outputs/anova_suitability_check.md`. If the recommended path is appropriate, create `config/human_review_decision.yaml` from `config/human_review_decision.example.yaml` and set:

```yaml
approval_status: approved
approved_analysis_path: classical_anova
```

Use `approved_analysis_path: welch_anova` if the reviewed recommendation is Welch ANOVA.

If the decision is `diagnostic_only` or `stop_analysis`, do not approve formal report generation without revising the data, analysis plan, or MVP scope.

Until approval is present, the workflow must not generate APA result paragraphs, formal statistical tables, result figures, or Word reports.
