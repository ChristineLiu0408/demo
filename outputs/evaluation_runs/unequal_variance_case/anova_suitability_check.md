# ANOVA Suitability Check

Generated: 2026-06-30 14:30

This diagnostic report is a statistical decision guardrail. It recommends an analysis path but does not authorize formal statistical reporting before human review.

## Overall Recommendation

- Overall decision: `welch_anova_recommended`
- Dataset rows: 200
- Grouping variable: `service_support_tool`
- Outcome variables: `resolution_efficiency`, `service_confidence`, `cognitive_load`

## Structural Checks

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `analysis_type` | `pass` | analysis_type: one_way_anova | Analysis type is supported. |
| `grouping_variable_present` | `pass` | grouping_variable: service_support_tool | Grouping variable is present. |
| `minimum_group_count` | `pass` | valid_group_count: 4<br>group_counts: {'No_Tool': 50, 'Knowledge_Base': 50, 'Chatbot_Copilot': 50, 'Agent_Copilot': 50} | At least two valid groups were found. |
| `expected_demo_groups` | `warning` | expected_groups: ['No_AI_Support', 'Basic_Chatbot', 'Workflow_Assistant', 'Agentic_Assistant']<br>unexpected_groups: ['Agent_Copilot', 'Chatbot_Copilot', 'Knowledge_Base', 'No_Tool']<br>missing_expected_groups: ['Agentic_Assistant', 'Basic_Chatbot', 'No_AI_Support', 'Workflow_Assistant'] | Group labels differ from the recommended demo groups. |
| `dependent_variables_present` | `pass` | outcomes: ['resolution_efficiency', 'service_confidence', 'cognitive_load'] | All dependent variables are present. |
| `dependent_variables_numeric` | `pass` | outcomes: ['resolution_efficiency', 'service_confidence', 'cognitive_load'] | All dependent variables are numeric. |
| `participant_id_unique` | `pass` | - | participant_id is unique when present. |
| `repeated_or_nested_structure` | `pass` | - | No repeated-measures or nested/cluster hint columns detected. |

## Outcome: `resolution_efficiency`

- Decision: `welch_anova_recommended`
- Recommended analysis after approval: `welch_anova`
- Recommended post hoc after approval: `games_howell`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'service_support_tool': 0.0, 'resolution_efficiency': 0.0}<br>group_missing_rates: {'Agent_Copilot': 0.0, 'Chatbot_Copilot': 0.0, 'Knowledge_Base': 0.0, 'No_Tool': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Agent_Copilot': 50, 'Chatbot_Copilot': 50, 'Knowledge_Base': 50, 'No_Tool': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.010<br>total_outliers: 2<br>by_group: {'Agent_Copilot': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.324, 'upper_fence': 8.634}, 'Chatbot_Copilot': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.584, 'upper_fence': 7.174}, 'Knowledge_Base': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 3.264, 'upper_fence': 5.334}, 'No_Tool': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.92, 'upper_fence': 4.94}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Agent_Copilot': {'n': 50, 'shapiro_w': 0.962, 'shapiro_p': 0.1078, 'skewness': -0.46, 'kurtosis': -0.346}, 'Chatbot_Copilot': {'n': 50, 'shapiro_w': 0.9797, 'shapiro_p': 0.5379, 'skewness': -0.244, 'kurtosis': 0.41}, 'Knowledge_Base': {'n': 50, 'shapiro_w': 0.9811, 'shapiro_p': 0.5995, 'skewness': 0.236, 'kurtosis': -0.032}, 'No_Tool': {'n': 50, 'shapiro_w': 0.9797, 'shapiro_p': 0.5412, 'skewness': 0.491, 'kurtosis': 0.734}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `warning` | levene_statistic: 22.745<br>levene_p: < .001<br>variance_by_group: {'Agent_Copilot': 1.1915, 'Chatbot_Copilot': 0.5752, 'Knowledge_Base': 0.2106, 'No_Tool': 0.14}<br>max_min_variance_ratio: 8.513<br>variance_violation: True<br>strong_warning: True | Strong variance heterogeneity warning; Welch ANOVA is recommended unless additional risks require diagnostic-only handling. |

## Outcome: `service_confidence`

- Decision: `welch_anova_recommended`
- Recommended analysis after approval: `welch_anova`
- Recommended post hoc after approval: `games_howell`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'service_support_tool': 0.0, 'service_confidence': 0.0}<br>group_missing_rates: {'Agent_Copilot': 0.0, 'Chatbot_Copilot': 0.0, 'Knowledge_Base': 0.0, 'No_Tool': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Agent_Copilot': 50, 'Chatbot_Copilot': 50, 'Knowledge_Base': 50, 'No_Tool': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.010<br>total_outliers: 2<br>by_group: {'Agent_Copilot': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.603, 'upper_fence': 7.603}, 'Chatbot_Copilot': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.278, 'upper_fence': 7.037}, 'Knowledge_Base': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 3.29, 'upper_fence': 5.37}, 'No_Tool': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.936, 'upper_fence': 4.786}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Agent_Copilot': {'n': 50, 'shapiro_w': 0.9703, 'shapiro_p': 0.2391, 'skewness': 0.041, 'kurtosis': -0.782}, 'Chatbot_Copilot': {'n': 50, 'shapiro_w': 0.9887, 'shapiro_p': 0.9108, 'skewness': 0.236, 'kurtosis': 0.106}, 'Knowledge_Base': {'n': 50, 'shapiro_w': 0.9816, 'shapiro_p': 0.6195, 'skewness': -0.231, 'kurtosis': 1.007}, 'No_Tool': {'n': 50, 'shapiro_w': 0.9711, 'shapiro_p': 0.257, 'skewness': 0.047, 'kurtosis': -0.85}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `warning` | levene_statistic: 18.524<br>levene_p: < .001<br>variance_by_group: {'Agent_Copilot': 0.8233, 'Chatbot_Copilot': 0.6958, 'Knowledge_Base': 0.1932, 'No_Tool': 0.0956}<br>max_min_variance_ratio: 8.609<br>variance_violation: True<br>strong_warning: True | Strong variance heterogeneity warning; Welch ANOVA is recommended unless additional risks require diagnostic-only handling. |

## Outcome: `cognitive_load`

- Decision: `welch_anova_recommended`
- Recommended analysis after approval: `welch_anova`
- Recommended post hoc after approval: `games_howell`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'service_support_tool': 0.0, 'cognitive_load': 0.0}<br>group_missing_rates: {'Agent_Copilot': 0.0, 'Chatbot_Copilot': 0.0, 'Knowledge_Base': 0.0, 'No_Tool': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Agent_Copilot': 50, 'Chatbot_Copilot': 50, 'Knowledge_Base': 50, 'No_Tool': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.005<br>total_outliers: 1<br>by_group: {'Agent_Copilot': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 0.47, 'upper_fence': 7.11}, 'Chatbot_Copilot': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.38, 'upper_fence': 6.32}, 'Knowledge_Base': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 3.186, 'upper_fence': 6.376}, 'No_Tool': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 4.506, 'upper_fence': 6.116}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Agent_Copilot': {'n': 50, 'shapiro_w': 0.9909, 'shapiro_p': 0.9645, 'skewness': 0.167, 'kurtosis': -0.316}, 'Chatbot_Copilot': {'n': 50, 'shapiro_w': 0.9826, 'shapiro_p': 0.6677, 'skewness': 0.079, 'kurtosis': -0.283}, 'Knowledge_Base': {'n': 50, 'shapiro_w': 0.9807, 'shapiro_p': 0.5831, 'skewness': 0.011, 'kurtosis': -0.803}, 'No_Tool': {'n': 50, 'shapiro_w': 0.989, 'shapiro_p': 0.9212, 'skewness': -0.34, 'kurtosis': 0.089}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `warning` | levene_statistic: 20.355<br>levene_p: < .001<br>variance_by_group: {'Agent_Copilot': 1.3703, 'Chatbot_Copilot': 0.6549, 'Knowledge_Base': 0.2772, 'No_Tool': 0.1007}<br>max_min_variance_ratio: 13.609<br>variance_violation: True<br>strong_warning: True | Strong variance heterogeneity warning; Welch ANOVA is recommended unless additional risks require diagnostic-only handling. |

## Guardrail Notes

- No missing values are automatically imputed.
- IQR outliers are flagged only; they are not automatically deleted.
- Shapiro-Wilk p < .05 is treated as a warning, not an automatic failure.
- Ordinary/classical ANOVA is used only when variance homogeneity is acceptable.
- When variance homogeneity is not met or is uncertain, the recommended path switches to Welch ANOVA with Games-Howell post hoc tests.
- Formal APA results, formal tables, figures, and Word reports must wait until human approval is recorded.
