# ANOVA Suitability Check

Generated: 2026-06-28 15:51

This diagnostic report is a statistical decision guardrail. It recommends an analysis path but does not authorize formal statistical reporting before human review.

## Overall Recommendation

- Overall decision: `classical_anova_recommended`
- Dataset rows: 200
- Grouping variable: `ai_support_condition`
- Outcome variables: `task_efficiency`, `work_confidence`, `perceived_workload`

## Structural Checks

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `analysis_type` | `pass` | analysis_type: one_way_anova | Analysis type is supported. |
| `grouping_variable_present` | `pass` | grouping_variable: ai_support_condition | Grouping variable is present. |
| `minimum_group_count` | `pass` | valid_group_count: 4<br>group_counts: {'No_AI_Support': 50, 'Basic_Chatbot': 50, 'Workflow_Assistant': 50, 'Agentic_Assistant': 50} | At least two valid groups were found. |
| `expected_demo_groups` | `pass` | expected_groups: ['No_AI_Support', 'Basic_Chatbot', 'Workflow_Assistant', 'Agentic_Assistant'] | All recommended demo groups are present. |
| `dependent_variables_present` | `pass` | outcomes: ['task_efficiency', 'work_confidence', 'perceived_workload'] | All dependent variables are present. |
| `dependent_variables_numeric` | `pass` | outcomes: ['task_efficiency', 'work_confidence', 'perceived_workload'] | All dependent variables are numeric. |
| `participant_id_unique` | `pass` | - | participant_id is unique when present. |
| `repeated_or_nested_structure` | `pass` | - | No repeated-measures or nested/cluster hint columns detected. |

## Outcome: `task_efficiency`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'ai_support_condition': 0.0, 'task_efficiency': 0.0}<br>group_missing_rates: {'Agentic_Assistant': 0.0, 'Basic_Chatbot': 0.0, 'No_AI_Support': 0.0, 'Workflow_Assistant': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Agentic_Assistant': 50, 'Basic_Chatbot': 50, 'No_AI_Support': 50, 'Workflow_Assistant': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.005<br>total_outliers: 1<br>by_group: {'Agentic_Assistant': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.87, 'upper_fence': 7.69}, 'Basic_Chatbot': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.099, 'upper_fence': 6.409}, 'No_AI_Support': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 1.326, 'upper_fence': 6.256}, 'Workflow_Assistant': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.38, 'upper_fence': 7.08}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Agentic_Assistant': {'n': 50, 'shapiro_w': 0.9727, 'shapiro_p': 0.2972, 'skewness': 0.21, 'kurtosis': -0.672}, 'Basic_Chatbot': {'n': 50, 'shapiro_w': 0.9824, 'shapiro_p': 0.6583, 'skewness': 0.098, 'kurtosis': 0.108}, 'No_AI_Support': {'n': 50, 'shapiro_w': 0.9702, 'shapiro_p': 0.2366, 'skewness': 0.104, 'kurtosis': -0.325}, 'Workflow_Assistant': {'n': 50, 'shapiro_w': 0.964, 'shapiro_p': 0.1302, 'skewness': 0.527, 'kurtosis': -0.274}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.066<br>levene_p: .978<br>variance_by_group: {'Agentic_Assistant': 0.7098, 'Basic_Chatbot': 0.7232, 'No_AI_Support': 0.7226, 'Workflow_Assistant': 0.7215}<br>max_min_variance_ratio: 1.019<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `work_confidence`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'ai_support_condition': 0.0, 'work_confidence': 0.0}<br>group_missing_rates: {'Agentic_Assistant': 0.0, 'Basic_Chatbot': 0.0, 'No_AI_Support': 0.0, 'Workflow_Assistant': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Agentic_Assistant': 50, 'Basic_Chatbot': 50, 'No_AI_Support': 50, 'Workflow_Assistant': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `warning` | overall_outlier_rate: 0.030<br>total_outliers: 6<br>by_group: {'Agentic_Assistant': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 3.237, 'upper_fence': 7.158}, 'Basic_Chatbot': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 1.854, 'upper_fence': 6.464}, 'No_AI_Support': {'n': 50, 'outliers': 4, 'outlier_rate': 0.08, 'lower_fence': 2.174, 'upper_fence': 5.344}, 'Workflow_Assistant': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.2, 'upper_fence': 7.3}} | Outliers are present and should be reviewed; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Agentic_Assistant': {'n': 50, 'shapiro_w': 0.9631, 'shapiro_p': 0.1196, 'skewness': -0.031, 'kurtosis': -0.608}, 'Basic_Chatbot': {'n': 50, 'shapiro_w': 0.9815, 'shapiro_p': 0.6186, 'skewness': 0.477, 'kurtosis': 0.19}, 'No_AI_Support': {'n': 50, 'shapiro_w': 0.9555, 'shapiro_p': 0.0578, 'skewness': 0.388, 'kurtosis': 1.867}, 'Workflow_Assistant': {'n': 50, 'shapiro_w': 0.9885, 'shapiro_p': 0.9047, 'skewness': -0.103, 'kurtosis': -0.268}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.213<br>levene_p: .887<br>variance_by_group: {'Agentic_Assistant': 0.7214, 'Basic_Chatbot': 0.7217, 'No_AI_Support': 0.7223, 'Workflow_Assistant': 0.724}<br>max_min_variance_ratio: 1.004<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `perceived_workload`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'ai_support_condition': 0.0, 'perceived_workload': 0.0}<br>group_missing_rates: {'Agentic_Assistant': 0.0, 'Basic_Chatbot': 0.0, 'No_AI_Support': 0.0, 'Workflow_Assistant': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Agentic_Assistant': 50, 'Basic_Chatbot': 50, 'No_AI_Support': 50, 'Workflow_Assistant': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.015<br>total_outliers: 3<br>by_group: {'Agentic_Assistant': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 1.874, 'upper_fence': 5.704}, 'Basic_Chatbot': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.575, 'upper_fence': 6.915}, 'No_AI_Support': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.706, 'upper_fence': 8.076}, 'Workflow_Assistant': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.256, 'upper_fence': 6.426}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Agentic_Assistant': {'n': 50, 'shapiro_w': 0.9727, 'shapiro_p': 0.297, 'skewness': 0.138, 'kurtosis': 1.222}, 'Basic_Chatbot': {'n': 50, 'shapiro_w': 0.985, 'shapiro_p': 0.7699, 'skewness': -0.034, 'kurtosis': 0.402}, 'No_AI_Support': {'n': 50, 'shapiro_w': 0.9762, 'shapiro_p': 0.4066, 'skewness': -0.081, 'kurtosis': -0.422}, 'Workflow_Assistant': {'n': 50, 'shapiro_w': 0.9847, 'shapiro_p': 0.7588, 'skewness': -0.132, 'kurtosis': -0.333}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.219<br>levene_p: .883<br>variance_by_group: {'Agentic_Assistant': 0.8092, 'Basic_Chatbot': 0.81, 'No_AI_Support': 0.8096, 'Workflow_Assistant': 0.8105}<br>max_min_variance_ratio: 1.002<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Guardrail Notes

- No missing values are automatically imputed.
- IQR outliers are flagged only; they are not automatically deleted.
- Shapiro-Wilk p < .05 is treated as a warning, not an automatic failure.
- Ordinary/classical ANOVA is used only when variance homogeneity is acceptable.
- When variance homogeneity is not met or is uncertain, the recommended path switches to Welch ANOVA with Games-Howell post hoc tests.
- Formal APA results, formal tables, figures, and Word reports must wait until human approval is recorded.
