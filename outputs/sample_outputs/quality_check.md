# 质量检查报告

本 QA 报告用于检查 workflow 是否遵守 human-in-the-loop 边界、是否使用了正确的数据和分析路径，以及生成的报告资产是否适合公开展示。

QA 采用分层设计：Hard QA 检查流程有效性和公开安全风险；Soft QA 检查稳定、可机器识别的报告规则；Editorial QA 记录需要人工审阅的表达和版式项目，避免把所有写作偏好都变成脆弱的自动规则。

## Workflow Gate

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| 人工确认 gate | `pass` | 3/3 个 outcome 包含已确认的分析路径。 | 暂停报告生成，并更新 outcome-level human review decision 文件。 |
| 正式输出发生在审批之后 | `pass` | 正式输出在 report stage 生成。 | 在所有必要审批记录完成前，不应生成正式报告资产。 |
| 未从阻断路径继续生成报告 | `pass` | 本次 report stage 没有从 diagnostic_only 或 stop_analysis 继续执行。 | 停止正式报告，只返回诊断建议。 |

## Data & Analysis Integrity

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| 指标覆盖 | `pass` | 配置 outcome 数量：3；实际分析 outcome 数量：3。 | 为缺失 outcome 重新运行分析，或更新 analysis plan。 |
| 分析路径一致性 | `pass` | ordinary ANOVA 对应 Tukey HSD；Welch ANOVA 对应 Games-Howell。 | 对齐每个 outcome 的 approved analysis path 和 post hoc method。 |
| 基准组和目标组 | `pass` | 基准组为无AI辅助，目标组为智能体AI辅助。 | 在 analysis_plan.yaml 中设置有效的 baseline_condition 和 focal_condition。 |
| 正式报告资产完整性 | `pass` | 已生成最终 Word 报告、中文业务报告、结果图、均值表和分析结果 JSON。 | 重新运行 report stage，并检查最终 Word 报告、图、表和分析结果 JSON。 |

## Statistical Reporting Quality

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| Omnibus 统计量 | `pass` | 每个 outcome 都包含 df、统计量、p 值和效应量。 | 使用 confirmed analysis runner 重新生成 analysis_results.json。 |
| APA 统计符号 | `pass` | Markdown 报告包含斜体 APA 统计符号。 | 重新生成带 APA 符号格式的结果段落。 |
| 百分比解释 | `pass` | 核心结果将智能体AI辅助与无AI辅助进行比较。 | 在核心结果中加入动态百分比解释。 |
| 正向与负向指标措辞 | `pass` | 核心百分比摘要区分了提高和降低。 | 检查 analysis_plan.yaml 中的 outcome_directions。 |

## Report Structure & Communication

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| 两段式报告结构 | `pass` | 报告使用“核心内容 + 详细统计报告”的结构。 | 恢复两段式报告结构。 |
| 核心内容小节 | `pass` | 核心内容拆分为报告目标、核心结果和行动建议。 | 在核心内容下补充三个必要小节。 |
| 表格位于详细统计报告中 | `pass` | 表 1 出现在详细统计报告部分。 | 将表 1 移到第 2 部分的方法说明段之后。 |
| 正式报告正文不突出 mock data 说明 | `pass` | 正式业务报告没有在正文开头突出 mock-data disclaimer。 | 将 mock data 说明保留在 README / privacy docs，而不是正式报告正文。 |

## Table & Figure QA

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| 图文件输出 | `pass` | outputs/figure_combined_raincloud.png | 重新生成组合 raincloud figure。 |
| 图题在图片上方 | `pass` | 图题作为报告正文出现在图片前，而不是嵌入图片内部。 | 在 Markdown 和 Word 中将图题移动到图片上方。 |
| 表题在表格上方 | `pass` | 表题出现在均值表前。 | 将表题移动到表格上方。 |
| 图注和表注 | `pass` | 图注和表注作为正文生成在对应图表下方。 | 重新生成图表下方的注释。 |

## Report Editorial QA

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| 核心结果可读性 | `manual` | 需要人工确认百分比解释是否自然融入核心结果段落，而不是机械单列。 | 修改报告模板或 report_context 文案，然后重新生成报告。 |
| 图表 block 呈现 | `manual` | 需要人工审阅每个图表是否作为一个整体呈现：标题、图/表、注释和周围留白。 | 调整 block spacing、caption 文案、图片尺寸或表格宽度。 |
| Word 渲染 QA | `manual` | 需要渲染 DOCX 并检查是否有孤立标题、表格拥挤、分页不自然或显著性标注重叠。 | 发布前调整 Word 间距、keep-with-next、图尺寸或表格宽度。 |

## Privacy & Public Showcase Safety

| 检查项 | 状态 | 证据 | 如果失败应如何处理 |
| --- | --- | --- | --- |
| 本地路径暴露 | `pass` | 文本输出中未发现本地绝对路径。 | 发布前将绝对路径替换为项目相对路径。 |
| 类密钥字符串 | `pass` | 未发现 API key、token、password 或类似密钥标记。 | 删除密钥，并轮换任何已暴露凭据。 |
| 个人联系信息泄露 | `pass` | 生成文本中未发现类似 email 的字符串。 | 删除个人联系信息，除非它是有意公开内容。 |

## Outcome Labels

- `task_efficiency`: 任务效率
- `work_confidence`: 工作信心
- `perceived_workload`: 感知工作负荷

## Guardrail Confirmation

- 在审批前，不应生成正式 APA-style 结果、正式表格、图或 Word 报告。
- 本次运行使用了 `config/human_review_decision.yaml` 中记录的 outcome-level approval。
- 本次运行中未出现 `diagnostic_only` 或 `stop_analysis` 阻断路径。
