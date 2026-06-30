# Sample Outputs

这里存放已经筛选过的 synthetic/mock 样例输出，用于 GitHub portfolio 展示。

最重要的文件：

- `final_report.docx`：最终 Word 报告样例。
- `business_friendly_report_zh.md`：中文业务报告 Markdown 版本。
- `figure_combined_raincloud.png`：三指标组合结果图。
- `mean_table_compact_letters.csv`：APA-style 均值表。
- `anova_suitability_check.md`：ANOVA 适用性检查。
- `human_review_required.md`：人工确认提示。
- `quality_check.md`：质量检查报告。
- `evaluation_report.md`：稳定性评估报告。

运行 `python -m src.evaluation_runner` 后，`outputs/evaluation_runs/` 会为可报告的 evaluation cases 生成 `final_report.docx`。这些 Word 报告用于后续人工评估 Human Edit Rate、Error Detection Rate 和 Time Saved；`diagnostic_only_case` 不应生成正式报告。

这些文件不代表真实业务结果或真实研究结果。
