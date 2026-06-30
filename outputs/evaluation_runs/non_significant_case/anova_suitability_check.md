# ANOVA Suitability Check

Generated: 2026-06-30 14:30

This diagnostic report is a statistical decision guardrail. It recommends an analysis path but does not authorize formal statistical reporting before human review.

## Overall Recommendation

- Overall decision: `classical_anova_recommended`
- Dataset rows: 200
- Grouping variable: `knowledge_search_interface`
- Outcome variables: `search_efficiency`, `decision_confidence`, `perceived_effort`

## Structural Checks

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `analysis_type` | `pass` | analysis_type: one_way_anova | Analysis type is supported. |
| `grouping_variable_present` | `pass` | grouping_variable: knowledge_search_interface | Grouping variable is present. |
| `minimum_group_count` | `pass` | valid_group_count: 4<br>group_counts: {'Standard_Search': 50, 'Tagged_Knowledge_Base': 50, 'Guided_Workflow': 50, 'AI_Summary_Interface': 50} | At least two valid groups were found. |
| `expected_demo_groups` | `warning` | expected_groups: ['No_AI_Support', 'Basic_Chatbot', 'Workflow_Assistant', 'Agentic_Assistant']<br>unexpected_groups: ['AI_Summary_Interface', 'Guided_Workflow', 'Standard_Search', 'Tagged_Knowledge_Base']<br>missing_expected_groups: ['Agentic_Assistant', 'Basic_Chatbot', 'No_AI_Support', 'Workflow_Assistant'] | Group labels differ from the recommended demo groups. |
| `dependent_variables_present` | `pass` | outcomes: ['search_efficiency', 'decision_confidence', 'perceived_effort'] | All dependent variables are present. |
| `dependent_variables_numeric` | `pass` | outcomes: ['search_efficiency', 'decision_confidence', 'perceived_effort'] | All dependent variables are numeric. |
| `participant_id_unique` | `pass` | - | participant_id is unique when present. |
| `repeated_or_nested_structure` | `pass` | - | No repeated-measures or nested/cluster hint columns detected. |

## Outcome: `search_efficiency`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'knowledge_search_interface': 0.0, 'search_efficiency': 0.0}<br>group_missing_rates: {'AI_Summary_Interface': 0.0, 'Guided_Workflow': 0.0, 'Standard_Search': 0.0, 'Tagged_Knowledge_Base': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'AI_Summary_Interface': 50, 'Guided_Workflow': 50, 'Standard_Search': 50, 'Tagged_Knowledge_Base': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.020<br>total_outliers: 4<br>by_group: {'AI_Summary_Interface': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.836, 'upper_fence': 5.606}, 'Guided_Workflow': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.846, 'upper_fence': 5.616}, 'Standard_Search': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.796, 'upper_fence': 5.566}, 'Tagged_Knowledge_Base': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.816, 'upper_fence': 5.586}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'AI_Summary_Interface': {'n': 50, 'shapiro_w': 0.9765, 'shapiro_p': 0.4155, 'skewness': 0.357, 'kurtosis': -0.138}, 'Guided_Workflow': {'n': 50, 'shapiro_w': 0.9765, 'shapiro_p': 0.4155, 'skewness': 0.357, 'kurtosis': -0.138}, 'Standard_Search': {'n': 50, 'shapiro_w': 0.9765, 'shapiro_p': 0.4155, 'skewness': 0.357, 'kurtosis': -0.138}, 'Tagged_Knowledge_Base': {'n': 50, 'shapiro_w': 0.9765, 'shapiro_p': 0.4155, 'skewness': 0.357, 'kurtosis': -0.138}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.000<br>levene_p: 1.000<br>variance_by_group: {'AI_Summary_Interface': 0.4303, 'Guided_Workflow': 0.4303, 'Standard_Search': 0.4303, 'Tagged_Knowledge_Base': 0.4303}<br>max_min_variance_ratio: 1.000<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `decision_confidence`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'knowledge_search_interface': 0.0, 'decision_confidence': 0.0}<br>group_missing_rates: {'AI_Summary_Interface': 0.0, 'Guided_Workflow': 0.0, 'Standard_Search': 0.0, 'Tagged_Knowledge_Base': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'AI_Summary_Interface': 50, 'Guided_Workflow': 50, 'Standard_Search': 50, 'Tagged_Knowledge_Base': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `warning` | overall_outlier_rate: 0.040<br>total_outliers: 8<br>by_group: {'AI_Summary_Interface': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 2.616, 'upper_fence': 5.646}, 'Guided_Workflow': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 2.636, 'upper_fence': 5.666}, 'Standard_Search': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 2.606, 'upper_fence': 5.636}, 'Tagged_Knowledge_Base': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 2.626, 'upper_fence': 5.656}} | Outliers are present and should be reviewed; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'AI_Summary_Interface': {'n': 50, 'shapiro_w': 0.9879, 'shapiro_p': 0.8848, 'skewness': -0.101, 'kurtosis': 0.427}, 'Guided_Workflow': {'n': 50, 'shapiro_w': 0.9879, 'shapiro_p': 0.8848, 'skewness': -0.101, 'kurtosis': 0.427}, 'Standard_Search': {'n': 50, 'shapiro_w': 0.9879, 'shapiro_p': 0.8848, 'skewness': -0.101, 'kurtosis': 0.427}, 'Tagged_Knowledge_Base': {'n': 50, 'shapiro_w': 0.9879, 'shapiro_p': 0.8848, 'skewness': -0.101, 'kurtosis': 0.427}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.000<br>levene_p: 1.000<br>variance_by_group: {'AI_Summary_Interface': 0.5513, 'Guided_Workflow': 0.5513, 'Standard_Search': 0.5513, 'Tagged_Knowledge_Base': 0.5513}<br>max_min_variance_ratio: 1.000<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `perceived_effort`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'knowledge_search_interface': 0.0, 'perceived_effort': 0.0}<br>group_missing_rates: {'AI_Summary_Interface': 0.0, 'Guided_Workflow': 0.0, 'Standard_Search': 0.0, 'Tagged_Knowledge_Base': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'AI_Summary_Interface': 50, 'Guided_Workflow': 50, 'Standard_Search': 50, 'Tagged_Knowledge_Base': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.020<br>total_outliers: 4<br>by_group: {'AI_Summary_Interface': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.587, 'upper_fence': 6.388}, 'Guided_Workflow': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.577, 'upper_fence': 6.377}, 'Standard_Search': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.628, 'upper_fence': 6.427}, 'Tagged_Knowledge_Base': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.597, 'upper_fence': 6.398}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'AI_Summary_Interface': {'n': 50, 'shapiro_w': 0.9787, 'shapiro_p': 0.4986, 'skewness': -0.512, 'kurtosis': 0.909}, 'Guided_Workflow': {'n': 50, 'shapiro_w': 0.9787, 'shapiro_p': 0.4986, 'skewness': -0.512, 'kurtosis': 0.909}, 'Standard_Search': {'n': 50, 'shapiro_w': 0.9787, 'shapiro_p': 0.4986, 'skewness': -0.512, 'kurtosis': 0.909}, 'Tagged_Knowledge_Base': {'n': 50, 'shapiro_w': 0.9787, 'shapiro_p': 0.4986, 'skewness': -0.512, 'kurtosis': 0.909}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.000<br>levene_p: 1.000<br>variance_by_group: {'AI_Summary_Interface': 0.5724, 'Guided_Workflow': 0.5724, 'Standard_Search': 0.5724, 'Tagged_Knowledge_Base': 0.5724}<br>max_min_variance_ratio: 1.000<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Guardrail Notes

- No missing values are automatically imputed.
- IQR outliers are flagged only; they are not automatically deleted.
- Shapiro-Wilk p < .05 is treated as a warning, not an automatic failure.
- Ordinary/classical ANOVA is used only when variance homogeneity is acceptable.
- When variance homogeneity is not met or is uncertain, the recommended path switches to Welch ANOVA with Games-Howell post hoc tests.
- Formal APA results, formal tables, figures, and Word reports must wait until human approval is recorded.
