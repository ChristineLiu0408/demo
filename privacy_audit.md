# Privacy Audit

This checklist must be completed before publishing the repository or sharing screenshots.

## Data

- [ ] Dataset is synthetic or mock data only.
- [ ] Variable names do not reveal real manuscripts, labs, collaborators, schools, companies, or projects.
- [ ] Sample sizes, means, and patterns are not copied from unpublished research.
- [ ] No raw participant-level real data is included.

## Configuration

- [ ] `analysis_plan.yaml` uses only synthetic scenario details.
- [ ] `human_review_decision.yaml` is not committed.
- [ ] No API keys, tokens, local usernames, or machine paths are present.

## Prompts

- [ ] Prompt templates are public-facing abstractions.
- [ ] No original private Codex Skill source text is copied.
- [ ] No manuscript excerpts or unpublished findings are included.

## Outputs

- [ ] Sample outputs are generated from synthetic data only.
- [ ] Word document metadata has been checked before public release.
- [ ] `outputs/sample_outputs/final_report.docx` is intentionally included as the core public report sample.
- [ ] `重点展示材料/01_最终报告样例_AI辅助试点.docx` is a public-safe copy of the final report, not a revision draft.
- [ ] `重点展示材料/` contains only curated showcase copies and no workflow input files.
- [ ] Figures and screenshots do not show local paths, private tabs, real names, or private files.

## Repository

- [ ] `.gitignore` blocks real data, local decisions, logs, caches, and environment files.
- [ ] `.local_deps/`, `.pytest_cache/`, `.mplconfig/`, `__pycache__/`, revision Word files, and temporary Word files are not included.
- [ ] Commit history does not contain sensitive files.
- [ ] README clearly states the project uses mock data and is a portfolio demo / workflow prototype.
