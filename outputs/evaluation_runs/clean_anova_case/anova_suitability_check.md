# ANOVA Suitability Check

Generated: 2026-06-30 14:30

This diagnostic report is a statistical decision guardrail. It recommends an analysis path but does not authorize formal statistical reporting before human review.

## Overall Recommendation

- Overall decision: `classical_anova_recommended`
- Dataset rows: 200
- Grouping variable: `onboarding_training_format`
- Outcome variables: `learning_effectiveness`, `onboarding_confidence`, `training_burden`

## Structural Checks

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `analysis_type` | `pass` | analysis_type: one_way_anova | Analysis type is supported. |
| `grouping_variable_present` | `pass` | grouping_variable: onboarding_training_format | Grouping variable is present. |
| `minimum_group_count` | `pass` | valid_group_count: 4<br>group_counts: {'Reading_Materials': 50, 'Recorded_Video': 50, 'Live_Workshop': 50, 'Mentor_Guided': 50} | At least two valid groups were found. |
| `expected_demo_groups` | `warning` | expected_groups: ['No_AI_Support', 'Basic_Chatbot', 'Workflow_Assistant', 'Agentic_Assistant']<br>unexpected_groups: ['Live_Workshop', 'Mentor_Guided', 'Reading_Materials', 'Recorded_Video']<br>missing_expected_groups: ['Agentic_Assistant', 'Basic_Chatbot', 'No_AI_Support', 'Workflow_Assistant'] | Group labels differ from the recommended demo groups. |
| `dependent_variables_present` | `pass` | outcomes: ['learning_effectiveness', 'onboarding_confidence', 'training_burden'] | All dependent variables are present. |
| `dependent_variables_numeric` | `pass` | outcomes: ['learning_effectiveness', 'onboarding_confidence', 'training_burden'] | All dependent variables are numeric. |
| `participant_id_unique` | `pass` | - | participant_id is unique when present. |
| `repeated_or_nested_structure` | `pass` | - | No repeated-measures or nested/cluster hint columns detected. |

## Outcome: `learning_effectiveness`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'onboarding_training_format': 0.0, 'learning_effectiveness': 0.0}<br>group_missing_rates: {'Live_Workshop': 0.0, 'Mentor_Guided': 0.0, 'Reading_Materials': 0.0, 'Recorded_Video': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Live_Workshop': 50, 'Mentor_Guided': 50, 'Reading_Materials': 50, 'Recorded_Video': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.015<br>total_outliers: 3<br>by_group: {'Live_Workshop': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 3.315, 'upper_fence': 6.135}, 'Mentor_Guided': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 3.21, 'upper_fence': 6.65}, 'Reading_Materials': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 1.958, 'upper_fence': 5.637}, 'Recorded_Video': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 2.696, 'upper_fence': 5.546}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Live_Workshop': {'n': 50, 'shapiro_w': 0.9674, 'shapiro_p': 0.1802, 'skewness': -0.377, 'kurtosis': -0.197}, 'Mentor_Guided': {'n': 50, 'shapiro_w': 0.9814, 'shapiro_p': 0.6107, 'skewness': 0.306, 'kurtosis': -0.419}, 'Reading_Materials': {'n': 50, 'shapiro_w': 0.969, 'shapiro_p': 0.2107, 'skewness': -0.53, 'kurtosis': -0.166}, 'Recorded_Video': {'n': 50, 'shapiro_w': 0.9845, 'shapiro_p': 0.7511, 'skewness': 0.217, 'kurtosis': 0.129}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.076<br>levene_p: .973<br>variance_by_group: {'Live_Workshop': 0.4872, 'Mentor_Guided': 0.3819, 'Reading_Materials': 0.4036, 'Recorded_Video': 0.4316}<br>max_min_variance_ratio: 1.276<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `onboarding_confidence`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'onboarding_training_format': 0.0, 'onboarding_confidence': 0.0}<br>group_missing_rates: {'Live_Workshop': 0.0, 'Mentor_Guided': 0.0, 'Reading_Materials': 0.0, 'Recorded_Video': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Live_Workshop': 50, 'Mentor_Guided': 50, 'Reading_Materials': 50, 'Recorded_Video': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.010<br>total_outliers: 2<br>by_group: {'Live_Workshop': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 2.802, 'upper_fence': 6.203}, 'Mentor_Guided': {'n': 50, 'outliers': 1, 'outlier_rate': 0.02, 'lower_fence': 3.445, 'upper_fence': 6.845}, 'Reading_Materials': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.018, 'upper_fence': 5.477}, 'Recorded_Video': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.277, 'upper_fence': 5.637}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Live_Workshop': {'n': 50, 'shapiro_w': 0.9788, 'shapiro_p': 0.5037, 'skewness': -0.411, 'kurtosis': 0.215}, 'Mentor_Guided': {'n': 50, 'shapiro_w': 0.9866, 'shapiro_p': 0.8359, 'skewness': -0.241, 'kurtosis': -0.159}, 'Reading_Materials': {'n': 50, 'shapiro_w': 0.9774, 'shapiro_p': 0.4485, 'skewness': 0.472, 'kurtosis': 0.016}, 'Recorded_Video': {'n': 50, 'shapiro_w': 0.9741, 'shapiro_p': 0.3356, 'skewness': 0.159, 'kurtosis': -0.563}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.143<br>levene_p: .934<br>variance_by_group: {'Live_Workshop': 0.478, 'Mentor_Guided': 0.4868, 'Reading_Materials': 0.442, 'Recorded_Video': 0.4218}<br>max_min_variance_ratio: 1.154<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Outcome: `training_burden`

- Decision: `classical_anova_recommended`
- Recommended analysis after approval: `classical_one_way_anova`
- Recommended post hoc after approval: `tukey_hsd`

| Check | Status | Key values | Interpretation |
| --- | --- | --- | --- |
| `missingness` | `pass` | variable_missing_rates: {'onboarding_training_format': 0.0, 'training_burden': 0.0}<br>group_missing_rates: {'Live_Workshop': 0.0, 'Mentor_Guided': 0.0, 'Reading_Materials': 0.0, 'Recorded_Video': 0.0} | Missingness is within the pass threshold; no automatic imputation is applied. |
| `group_sample_size` | `pass` | valid_n_by_group: {'Live_Workshop': 50, 'Mentor_Guided': 50, 'Reading_Materials': 50, 'Recorded_Video': 50}<br>min_group_n: 50 | Every group has at least 20 valid cases. |
| `sample_size_balance` | `pass` | max_n: 50<br>min_n: 50<br>max_to_min_ratio: 1.000 | Group sample sizes are acceptably balanced. |
| `outliers_iqr` | `pass` | overall_outlier_rate: 0.010<br>total_outliers: 2<br>by_group: {'Live_Workshop': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 2.744, 'upper_fence': 6.154}, 'Mentor_Guided': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 1.884, 'upper_fence': 5.854}, 'Reading_Materials': {'n': 50, 'outliers': 2, 'outlier_rate': 0.04, 'lower_fence': 3.551, 'upper_fence': 6.781}, 'Recorded_Video': {'n': 50, 'outliers': 0, 'outlier_rate': 0.0, 'lower_fence': 3.121, 'upper_fence': 6.251}} | Outlier rate is within the pass threshold; no automatic deletion is applied. |
| `normality` | `pass` | by_group: {'Live_Workshop': {'n': 50, 'shapiro_w': 0.9898, 'shapiro_p': 0.9417, 'skewness': 0.025, 'kurtosis': -0.096}, 'Mentor_Guided': {'n': 50, 'shapiro_w': 0.9949, 'shapiro_p': 0.9989, 'skewness': -0.128, 'kurtosis': -0.016}, 'Reading_Materials': {'n': 50, 'shapiro_w': 0.9842, 'shapiro_p': 0.7371, 'skewness': -0.133, 'kurtosis': 0.173}, 'Recorded_Video': {'n': 50, 'shapiro_w': 0.9667, 'shapiro_p': 0.1691, 'skewness': 0.256, 'kurtosis': -0.565}} | No severe group-level normality issue detected. |
| `variance_homogeneity` | `pass` | levene_statistic: 0.360<br>levene_p: .782<br>variance_by_group: {'Live_Workshop': 0.4125, 'Mentor_Guided': 0.494, 'Reading_Materials': 0.551, 'Recorded_Video': 0.4153}<br>max_min_variance_ratio: 1.336<br>variance_violation: False<br>strong_warning: False | Variance homogeneity is acceptable; classical ANOVA is eligible. |

## Guardrail Notes

- No missing values are automatically imputed.
- IQR outliers are flagged only; they are not automatically deleted.
- Shapiro-Wilk p < .05 is treated as a warning, not an automatic failure.
- Ordinary/classical ANOVA is used only when variance homogeneity is acceptable.
- When variance homogeneity is not met or is uncertain, the recommended path switches to Welch ANOVA with Games-Howell post hoc tests.
- Formal APA results, formal tables, figures, and Word reports must wait until human approval is recorded.
