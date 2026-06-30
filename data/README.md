# Data

This folder contains synthetic data for the showcase workflow.

## MVP Dataset

- `employee_ai_support_mock.csv`

This file is synthetic/mock data for a fictional workplace AI productivity scenario. It does not correspond to any real study, real participant, real company, unpublished dataset, collaborator, or manuscript.

## Study Design

- Total sample size: N = 200
- Design: between-subjects one-way ANOVA demo
- Grouping variable: `ai_support_condition`
- Conditions: `No_AI_Support`, `Basic_Chatbot`, `Workflow_Assistant`, `Agentic_Assistant`
- Per-group sample size: n = 50

## Outcome Variables

All outcome variables are continuous 1-7 scale scores rounded to two decimals.

- `task_efficiency`
- `work_confidence`
- `perceived_workload`

## Expected Mean Pattern

The synthetic data is generated to support a clean first-version workflow demo:

| ai_support_condition | task_efficiency | work_confidence | perceived_workload |
| --- | ---: | ---: | ---: |
| No_AI_Support | 3.80 | 3.70 | 5.30 |
| Basic_Chatbot | 4.30 | 4.20 | 4.80 |
| Workflow_Assistant | 4.85 | 4.70 | 4.30 |
| Agentic_Assistant | 5.35 | 5.20 | 3.80 |

Expected trends:

- `task_efficiency`: increases as AI support becomes more advanced.
- `work_confidence`: increases as AI support becomes more advanced.
- `perceived_workload`: decreases as AI support becomes more advanced.

## Generation Notes

- Fixed random seed: `20260627`
- Per-group standard deviation target: approximately 0.85 for `task_efficiency` and `work_confidence`; approximately 0.90 for `perceived_workload`
- Values are generated from normal distributions and constrained to the 1-7 range.
- No missing values are included.
- No severe outliers are intentionally generated.
