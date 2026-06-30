# ANOVA Suitability Check

Generated: 2026-06-30 14:30

This diagnostic report is a statistical decision guardrail. It recommends an analysis path but does not authorize formal statistical reporting before human review.

## Overall Recommendation

- Overall decision: `diagnostic_only`
- Dataset rows: 32
- Grouping variable: `training_format`
- Outcome variables: `knowledge_mastery`, `transfer_confidence`, `training_fatigue`

## Structural Checks

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `analysis_type` | `pass` | analysis_type: one_way_anova | Analysis type is supported. |
| `grouping_variable_present` | `pass` | grouping_variable: training_format | Grouping variable is present. |
| `minimum_group_count` | `pass` | valid_group_count: 4<br>group_counts: {'Self_Study': 8, 'Live_Workshop': 8, 'Blended_Coaching': 8, 'AI_Tutor': 8} | At least two valid groups were found. |
| `expected_demo_groups` | `warning` | expected_groups: ['No_AI_Support', 'Basic_Chatbot', 'Workflow_Assistant', 'Agentic_Assistant']<br>unexpected_groups: ['AI_Tutor', 'Blended_Coaching', 'Live_Workshop', 'Self_Study']<br>missing_expected_groups: ['Agentic_Assistant', 'Basic_Chatbot', 'No_AI_Support', 'Workflow_Assistant'] | Group labels differ from the recommended demo groups. |
| `dependent_variables_present` | `pass` | outcomes: ['knowledge_mastery', 'transfer_confidence', 'training_fatigue'] | All dependent variables are present. |
| `dependent_variables_numeric` | `pass` | outcomes: ['knowledge_mastery', 'transfer_confidence', 'training_fatigue'] | All dependent variables are numeric. |
| `participant_id_unique` | `pass` | - | participant_id is unique when present. |
| `repeated_or_nested_structure` | `pass` | - | No repeated-measures or nested/cluster hint columns detected. |

## Outcome: `knowledge_mastery`

- Decision: `diagnostic_only`
- Recommended analysis after approval: `none`
- Recommended post hoc after approval: `none`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'training_format': 0.0, 'knowledge_mastery': 0.0}<br>group_missing_rates: {'AI_Tutor': 0.0, 'Blended_Coaching': 0.0, 'Live_Workshop': 0.0, 'Self_Study': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `diagnostic_only` | valid_n_by_group: {'AI_Tutor': 8, 'Blended_Coaching': 8, 'Live_Workshop': 8, 'Self_Study': 8}<br>min_group_n: 8 | At least one group has fewer than 10 valid cases. |
| `sample_size_balance` | `pass` | max_n: 8<br>min_n: 8<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.000<br>total_outliers: 0<br>by_group: {'AI_Tutor': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.898, 'upper_fence': 7.277}, 'Blended_Coaching': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 3.086, 'upper_fence': 6.356}, 'Live_Workshop': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 0.931, 'upper_fence': 6.301}, 'Self_Study': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 1.3, 'upper_fence': 5.82}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'AI_Tutor': {'n': 8, 'shapiro_w': 0.9144, 'shapiro_p': 0.386, 'skewness': -0.987, 'kurtosis': 0.263}, 'Blended_Coaching': {'n': 8, 'shapiro_w': 0.8922, 'shapiro_p': 0.2453, 'skewness': 0.184, 'kurtosis': -1.697}, 'Live_Workshop': {'n': 8, 'shapiro_w': 0.915, 'shapiro_p': 0.3904, 'skewness': -0.68, 'kurtosis': -0.841}, 'Self_Study': {'n': 8, 'shapiro_w': 0.9376, 'shapiro_p': 0.5874, 'skewness': -0.637, 'kurtosis': -0.263}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `warning` | levene_statistic: 0.475<br>levene_p: .702<br>variance_by_group: {'AI_Tutor': 0.8183, 'Blended_Coaching': 0.315, 'Live_Workshop': 1.1178, 'Self_Study': 0.6233}<br>max_min_variance_ratio: 3.548<br>variance_violation: True<br>strong_warning: False | Variance homogeneity is not met or is uncertain; Welch ANOVA is recommended. |

## Outcome: `transfer_confidence`

- Decision: `diagnostic_only`
- Recommended analysis after approval: `none`
- Recommended post hoc after approval: `none`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'training_format': 0.0, 'transfer_confidence': 0.0}<br>group_missing_rates: {'AI_Tutor': 0.0, 'Blended_Coaching': 0.0, 'Live_Workshop': 0.0, 'Self_Study': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `diagnostic_only` | valid_n_by_group: {'AI_Tutor': 8, 'Blended_Coaching': 8, 'Live_Workshop': 8, 'Self_Study': 8}<br>min_group_n: 8 | At least one group has fewer than 10 valid cases. |
| `sample_size_balance` | `pass` | max_n: 8<br>min_n: 8<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `diagnostic_only` | overall_outlier_rate: 0.062<br>total_outliers: 2<br>by_group: {'AI_Tutor': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 1.581, 'upper_fence': 8.951}, 'Blended_Coaching': {'n': 8, 'outliers': 1, 'outlier_rate': 0.125, 'lower_fence': 2.839, 'upper_fence': 6.369}, 'Live_Workshop': {'n': 8, 'outliers': 1, 'outlier_rate': 0.125, 'lower_fence': 3.692, 'upper_fence': 5.913}, 'Self_Study': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': -0.14, 'upper_fence': 7.46}} | Outlier pattern requires diagnostic-only handling and human review. |
| `normality` | `diagnostic_only` | by_group: {'AI_Tutor': {'n': 8, 'shapiro_w': 0.9425, 'shapiro_p': 0.6355, 'skewness': 0.326, 'kurtosis': -1.298}, 'Blended_Coaching': {'n': 8, 'shapiro_w': 0.9375, 'shapiro_p': 0.587, 'skewness': -0.991, 'kurtosis': 1.654}, 'Live_Workshop': {'n': 8, 'shapiro_w': 0.8654, 'shapiro_p': 0.1359, 'skewness': -1.144, 'kurtosis': 2.538}, 'Self_Study': {'n': 8, 'shapiro_w': 0.857, 'shapiro_p': 0.112, 'skewness': -0.496, 'kurtosis': -1.845}} | Normality risk is high enough that the workflow should not auto-generate formal conclusions. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.458<br>levene_p: .714<br>variance_by_group: {'AI_Tutor': 1.2522, 'Blended_Coaching': 0.7383, 'Live_Workshop': 0.956, 'Self_Study': 1.1685}<br>max_min_variance_ratio: 1.696<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `training_fatigue`

- Decision: `diagnostic_only`
- Recommended analysis after approval: `none`
- Recommended post hoc after approval: `none`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'training_format': 0.0, 'training_fatigue': 0.0}<br>group_missing_rates: {'AI_Tutor': 0.0, 'Blended_Coaching': 0.0, 'Live_Workshop': 0.0, 'Self_Study': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `diagnostic_only` | valid_n_by_group: {'AI_Tutor': 8, 'Blended_Coaching': 8, 'Live_Workshop': 8, 'Self_Study': 8}<br>min_group_n: 8 | At least one group has fewer than 10 valid cases. |
| `sample_size_balance` | `pass` | max_n: 8<br>min_n: 8<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `diagnostic_only` | overall_outlier_rate: 0.125<br>total_outliers: 4<br>by_group: {'AI_Tutor': {'n': 8, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.763, 'upper_fence': 5.702}, 'Blended_Coaching': {'n': 8, 'outliers': 2, 'outlier_rate': 0.25, 'lower_fence': 2.974, 'upper_fence': 6.964}, 'Live_Workshop': {'n': 8, 'outliers': 1, 'outlier_rate': 0.125, 'lower_fence': 1.588, 'upper_fence': 6.027}, 'Self_Study': {'n': 8, 'outliers': 1, 'outlier_rate': 0.125, 'lower_fence': 3.7, 'upper_fence': 6.14}} | Outlier pattern requires diagnostic-only handling and human review. |
| `normality` | `diagnostic_only` | by_group: {'AI_Tutor': {'n': 8, 'shapiro_w': 0.9043, 'shapiro_p': 0.316, 'skewness': 0.761, 'kurtosis': -0.281}, 'Blended_Coaching': {'n': 8, 'shapiro_w': 0.9259, 'shapiro_p': 0.4791, 'skewness': -0.348, 'kurtosis': 1.619}, 'Live_Workshop': {'n': 8, 'shapiro_w': 0.8679, 'shapiro_p': 0.1437, 'skewness': 1.403, 'kurtosis': 2.482}, 'Self_Study': {'n': 8, 'shapiro_w': 0.9274, 'shapiro_p': 0.4924, 'skewness': 0.504, 'kurtosis': -0.132}} | Normality risk is high enough that the workflow should not auto-generate formal conclusions. |
| `variance_homogeneity` | `warning` | levene_statistic: 0.319<br>levene_p: .812<br>variance_by_group: {'AI_Tutor': 0.611, 'Blended_Coaching': 1.8476, 'Live_Workshop': 1.233, 'Self_Study': 0.763}<br>max_min_variance_ratio: 3.024<br>variance_violation: True<br>strong_warning: False | Variance homogeneity is not met or is uncertain; Welch ANOVA is recommended. |

## Guardrail Notes

- No missing values are automatically imputed.
- IQR outliers are flagged only; they are not automatically deleted.
- Shapiro-Wilk p < .05 is treated as a warning, not an automatic failure.
- Ordinary/classical ANOVA is used only when variance homogeneity is acceptable.
- When variance homogeneity is not met or is uncertain, the recommended path switches to Welch ANOVA with Games-Howell post hoc tests.
- Formal APA results, formal tables, figures, and Word reports must wait until human approval is recorded.
