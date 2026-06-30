# Human Review Required

The suitability check has finished. The workflow is intentionally paused before formal statistical reporting.

- Overall recommendation: `classical_anova_recommended`
- Approval file required: `config/human_review_decision.yaml`

## Outcome-Level Recommendations

| Outcome | Decision | Analysis path | Post hoc |
| --- | --- | --- | --- |
| `task_efficiency` | `classical_anova_recommended` | `classical_one_way_anova` | `tukey_hsd` |
| `work_confidence` | `classical_anova_recommended` | `classical_one_way_anova` | `tukey_hsd` |
| `perceived_workload` | `classical_anova_recommended` | `classical_one_way_anova` | `tukey_hsd` |

## Required Human Action

Review `outputs/anova_suitability_check.md`. If the recommended path is appropriate, create `config/human_review_decision.yaml` from `config/human_review_decision.example.yaml` and set:

```yaml
approval_status: approved
approved_analysis_path: classical_anova
```

Use `approved_analysis_path: welch_anova` if the reviewed recommendation is Welch ANOVA.

If the decision is `diagnostic_only` or `stop_analysis`, do not approve formal report generation without revising the data, analysis plan, or MVP scope.

Until approval is present, the workflow must not generate APA result paragraphs, formal statistical tables, result figures, or Word reports.
