# APA Result Prompt Contract

Purpose: convert verified statistical outputs into a concise APA-style result paragraph.

Inputs:

- confirmed analysis path
- descriptive statistics
- ANOVA or Welch ANOVA result
- post-hoc comparison results
- variable labels from the analysis plan

Constraints:

- do not invent statistical values
- do not state formal conclusions before human approval
- use only values produced by the Python analysis runner
- keep wording suitable for a social science manuscript results section
