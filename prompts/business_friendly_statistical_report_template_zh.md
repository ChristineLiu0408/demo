# 中文业务友好统计报告模板

本文件用于指导 workflow 生成中文版、业务友好、但保留统计严谨性的 one-way ANOVA / Welch ANOVA 报告。

这是一般化报告模板，不是具体报告样例。不要写死真实研究主题、真实变量、真实结果、真实组织、真实参与者或未发表内容。所有具体内容应由 workflow 根据 synthetic/mock data、analysis plan、suitability check、human review decision 和统计结果自动填入。

如果本模板与当前项目对话中的规则不一致，以当前项目规则为准。

## 1. 报告定位

报告读者是假设的 AI 产品经理、业务负责人、运营同事、项目负责人或非统计背景的面试官。

报告目标不是写成学术论文结果部分，而是写成一份业务分析报告。报告应先告诉读者：

1. 本次分析想回答什么问题；
2. 核心发现是什么；
3. 图中能看到什么趋势；
4. 统计方法为什么这样选；
5. 主效应是否显著；
6. 哪些组之间存在显著差异；
7. 当前结果可以如何服务于后续工作调整。

## 2. 通用占位符

- `{analysis_title}`：报告标题
- `{analysis_goal}`：分析目标
- `{data_note}`：数据说明
- `{grouping_variable}`：分组变量名称
- `{grouping_variable_label}`：分组变量的中文标签
- `{group_labels}`：所有组别名称
- `{outcome_list}`：多个结果变量列表
- `{outcome_variable}`：单个结果变量名称
- `{outcome_label}`：单个结果变量的中文标签
- `{key_outcome_summary}`：核心结果指标摘要
- `{recommended_method}`：推荐统计方法
- `{posthoc_method}`：事后比较方法
- `{suitability_decision}`：suitability check 的总体判断
- `{human_review_status}`：人工确认状态
- `{omnibus_result}`：主效应检验结果，例如 `F(3, 196) = 8.42, p < .001`
- `{effect_size}`：效应量，例如 `η² = .11`
- `{descriptive_pattern}`：描述性统计趋势
- `{plain_language_pattern}`：通俗语言总结的结果模式
- `{significant_pairwise_comparisons}`：显著组间比较
- `{non_significant_pairwise_comparisons}`：不显著组间比较
- `{figure_reference}`：图示引用
- `{mean_table_reference}`：均值表引用
- `{business_interpretation}`：结果的实际含义
- `{decision_context}`：该结果可以服务的工作场景
- `{next_steps}`：下一步建议
- `{caution_note}`：由 suitability check 或 quality check 触发的谨慎解释提醒

## 3. 第一版 MVP 输出范围

第一版 MVP 支持 between-subjects one-way ANOVA 场景。报告应覆盖 `analysis_plan.yaml` 中配置的所有 outcome。

当前 GitHub showcase 的 sample config 使用三个 outcome：`task_efficiency`、`work_confidence` 和 `perceived_workload`。这只是 demo 样例，不是通用模板规则。换成其他 one-way ANOVA 场景时，应通过 `analysis_plan.yaml` 更新 grouping variable、condition labels、outcome labels、outcome directions、baseline condition、focal condition 和业务文案。

所有配置的 outcome 都需要运行 suitability check、人工确认、正式统计分析和结果报告。

如果三个 outcome 的 suitability recommendation 不一致，应按 outcome 分别记录 human review decision 和 approved analysis path。

## 4. 报告整体结构

# {analysis_title}

正式业务报告正文中不写 synthetic/mock data 开头说明。公开展示安全说明保留在 README、privacy audit 和项目文档中。

---

## 1. 核心内容

这一部分必须放在报告最开头。目标是让非统计背景读者快速理解：当前试点做了什么、想回答什么问题、核心发现是什么，以及结果可以如何指导后续工作。

### 1.1 报告目标

开头段应由 `report_context.overview_sentence` 或等价字段生成。通用要求是说明：

- 本次比较了哪些组别；
- 分析了哪些 outcome；
- 结果服务于什么工作或研究决策；
- 如果样本量适合简要说明，可以写明各组样本量。

当前 AI 辅助 sample 的开头段示例：

本次AI辅助工具试点随机试验和对比了四组员工的 `{outcome_list}`，以评估当前AI辅助工具试点方案的效果，并为后续的工作流优化提供建议。具体而言，随机分配员工到4种不同程度的AI辅助条件，各条件 `{n_per_group}` 人，包括 `{group_labels}`。

问题句应由 `report_context.questions` 生成。通用要求是：问题句可以体现业务或研究目标，但不要写死当前 AI 辅助场景。

当前 AI 辅助 sample 的问题示例：

本次分析希望回答两个问题：

1. AI辅助是否能提升员工的任务效率、工作信心，并降低员工的工作负荷？
2. 何种类型的AI辅助最有效，AI辅助的程度是越深越好吗？

### 1.2 核心结果

核心结果应由统计结果和 `report_context.core_findings` 共同生成。通用要求是：

- 先用自然语言总结组间差异方向；
- 将相对 baseline condition 的百分比解释融入核心结论段落，不要单独机械罗列成一个短段；
- 正向 outcome 使用“提升”，负向 outcome 使用“降低”；
- 百分比使用 `analysis_plan.yaml` 中配置的 `baseline_condition` 和 `focal_condition`，不得硬编码具体组名；
- 数值必须来自当前分析结果。

当前 AI 辅助 sample 的核心结论示例：

第一，所有的AI辅助均有效。三种AI辅助都能提升员工的任务效率、工作信心，降低员工的工作负荷感。

第二，AI辅助程度越深，效果越好。随着AI辅助的深度提高，也就是从对话AI辅助升级到工作流AI辅助再升级到智能体AI辅助，员工的任务效率和工作信心的提升越高，工作负荷感降低得越低。其中，`{focal_condition}` 相较 `{baseline_condition}` 可以提升 `{positive_outcome_percentage_summary}`，降低 `{negative_outcome_percentage_summary}`。

上述结果说明，AI辅助的程度越高，越能解放员工，提升组织效率。示例图见图1。

图直接放在核心结果附近，不单独建立“核心趋势图”小节。

图标题规则：

- 图题应优先简洁、业务友好，避免过长；
- 如果 `report_context.figure_title` 已配置，直接使用该图题；
- 如果未配置，则使用通用图题模板。

当前 AI 辅助 sample 图题：

**图 1. 不同AI辅助工具的效果**

通用图题模板：

**图 1. 不同 `{grouping_variable_label}` 下 `{outcome_count}` 个结果指标的分布与均值趋势**

图形规格：

- 使用 manuscript-ready 风格；
- 三个 outcome 放在同一张图中，建议横向排列为三个 panel；
- 每个 panel 展示一个 outcome；
- 每个 panel 使用相同的 1-7 y 轴范围；
- 条件顺序应固定为 `{group_labels}`；
- 图形元素建议包括 jittered individual observations、boxplot、half-violin distribution；
- 可加入显著组间比较 brackets；
- brackets 只显示通过 post hoc 检验确认的显著比较；
- brackets 高度使用固定逻辑：相邻比较同高；`无AI辅助-工作流AI辅助` 次高；`无AI辅助-智能体AI辅助` 更高；`对话AI辅助-智能体AI辅助` 最高；
- 显著性标记使用 `* p < .05; ** p < .01; *** p < .001`；
- 图片内部不要放总标题和图注；图标题和图注用 Word/Markdown 正文呈现；
- 图片内部保留三个 panel 标题。
- 图表 block 是一个整体，包括标题、图/表内容和注释；
- 图表 block 前后应留出视觉空行；
- block 内部不要在标题和内容之间、内容和注释之间插入过大的空白。

### 1.3 行动建议

行动建议应由 `report_context.action_recommendations` 或等价字段生成。通用要求是把统计发现转化为后续试点、资源投入、流程优化、指标追踪或人工复核建议。不要在通用模板里写死当前 AI 辅助业务场景。

当前 AI 辅助 sample 的行动建议示例：

未来企业可以继续推广AI辅助工具。尽管智能体AI的效果最优秀，但是各部门需要结合成本、员工接受度和业务目标选择最合适的AI辅助工具。

未来AI应用团队可以进一步了解员工的真实使用体验，并考察不同AI辅助工具的任务耗时、完成质量、用户反馈、使用频率和实施成本，继续积累推广经验。

---

## 2. 详细统计报告

这一部分提供支持核心结论的统计依据。结构应先说明方法选择，再放表 1，然后以连续段落报告所有配置的 outcome。

普通单因素方差分析模板：

在正式分析前，workflow 对数据结构、缺失值、组别样本量、异常值、正态性指标和方差齐性进行了检查。检查结果显示，当前数据基本满足 `{recommended_method}` 的使用条件。于是，经人工确认后，workflow 对 `{outcome_count}` 个结果指标均采用 `{recommended_method}`，并使用 `{posthoc_method}` 进行事后比较。各组均值、标准差和显著性字母标记见表 1。

Welch ANOVA 模板：

在正式分析前，workflow 对数据结构、缺失值、组别样本量、异常值、正态性指标和方差齐性进行了检查。检查结果显示，方差齐性假设未得到充分支持。因此，workflow 不采用普通单因素方差分析，而是推荐 Welch ANOVA，并在人工确认后使用 `{posthoc_method}` 进行事后比较。

仅输出诊断报告模板：

在正式分析前，workflow 识别出若干会影响统计结论可靠性的风险。因此，本报告不输出正式的推断性统计结论，而是仅汇总数据诊断结果，并提示用户进行人工检查或考虑替代分析方法。

结果段落模板：

单因素方差分析显示，`{grouping_variable_label}` 对 `{outcome_label}` 的影响显著，`{omnibus_result}`，`{effect_size}`。事后比较结果显示，不同组别在 `{outcome_label}` 上存在明显差异，`ps < .05`。具体而言，`{ordered_mean_sentence}`。相较 `{baseline_condition_label}`，`{focal_condition_label}` 使 `{outcome_label}` `{increase_or_decrease}` 约 `{percentage_change}`%。

结果段落规则：

- 不把每个因变量作为小标题；
- 以因变量为单位连续分段报告；
- 段落间使用自然连接词；
- 提升/下降百分比以 `baseline_condition` 为基准；
- 对负向指标使用下降百分比，例如 `(baseline - focal) / baseline * 100`。

第一版报告只生成一个均值表，不单独生成完整 pairwise comparison table。

正文模板：

事后比较采用 `{posthoc_method}`。结果显示，`{significant_pairwise_comparisons}`。其余比较未达到统计显著水平：`{non_significant_pairwise_comparisons}`。各组均值、标准差和显著性字母标记见 `{mean_table_reference}`。

如果 Welch ANOVA 被采用，则需要写：

由于方差齐性假设未得到充分支持，本报告采用 Welch ANOVA，并使用 Games-Howell 进行事后比较，而不是使用普通 ANOVA 和 Tukey HSD。

均值表标题模板：

**表 1. 不同 `{grouping_variable_label}` 下各结果指标的描述性统计**

均值表结构：

| 结果指标 | {group_1} | {group_2} | {group_3} | {group_4} |
| --- | ---: | ---: | ---: | ---: |
| `{outcome_label_1}` | `{M_1}``{letters}` (`{SD_1}`) | `{M_2}``{letters}` (`{SD_2}`) | `{M_3}``{letters}` (`{SD_3}`) | `{M_4}``{letters}` (`{SD_4}`) |

表格规则：

- 单元格格式为 `M_subscript (SD)`；
- `M` 和 `SD` 保留两位小数；
- 字母下标使用 compact letter display；
- 不共享同一字母的组别表示事后比较差异显著；
- 字母应基于当前 outcome 的 post hoc 结果分别计算；
- 如果某 outcome 的主效应不显著，可以不给字母下标，或所有组共享同一字母；
- 表格采用 APA 三线表风格；
- 不使用竖线、内部网格线或彩色底纹；
- 表下注释必须说明字母下标含义、量表范围和 post hoc 方法。

表下注释模板：

注：数值为均值，括号内为标准差。所有指标均为 1-7 分量表。每一行内，不共享相同字母下标的组别在事后比较中差异显著，p < .05。事后比较方法根据 suitability check 和人工确认结果确定。

---

## 3. 质量检查框架

生成报告后，workflow 应输出 `quality_check.md`。质检不是简单检查文件是否存在，而是确认这份报告是否在正确的人类确认边界内，用正确的数据、正确的方法、正确的表达，生成了可公开展示的结果。

质检应避免膨胀为所有写作偏好的清单。建议分为三层：

1. Hard QA：流程、统计和公开安全的关键风险，失败应阻止或标红；
2. Soft QA：机器能稳定检查的报告规则，通常输出 pass/warning；
3. Editorial QA：表达自然度和 Word 版式质感，由模板约束和人工渲染检查记录，不把每个偏好都写成自动 fail。

当前质检主体组织为六个模块：

1. Workflow Gate：人工确认与流程边界；
2. Data & Analysis Integrity：数据、analysis plan、方法和结果一致性；
3. Statistical Reporting Quality：APA 格式、p 值、效应量、百分比方向；
4. Report Structure & Communication：核心内容、详细统计报告、读者友好表达；
5. Table & Figure QA：图表标题位置、三线表、compact letters、brackets、图文一致性；
6. Privacy & Public Showcase Safety：脱敏、本地路径、真实数据和密钥风险。

另外可保留一个轻量 `Report Editorial QA`，只记录少数人工复核项，例如核心结果是否自然、图表 block 是否舒服、Word 渲染后是否存在孤立标题或分页问题。每个模块用小表呈现 `Check / Status / Evidence / Action if Failed`。

## 4. 行动推荐写作规则

行动推荐将统计结果转化为可执行建议。不要只重复统计显著性，而要说明这些结果可以如何用于后续产品、流程、运营、管理或研究决策。

行动推荐部分不要出现“如果这是实际业务数据”“如果该结果来自真实业务数据”等表达。synthetic/mock data 的限制说明只在 README、privacy audit 和项目文档中呈现，不要在正式业务报告中反复打断读者。

### 3.1 显著结果的行动推荐模板

基于当前结果，`{grouping_variable_label}` 的不同水平在 `{outcome_label}` 上存在明显差异。这说明 `{business_interpretation}`。团队可以将表现较好的组别方案作为后续试点方向，并继续追踪任务耗时、用户反馈、使用频率、转化率或其他关键业务指标，以判断该方案是否具有持续推广价值。

### 3.2 不显著结果的行动推荐模板

基于当前结果，尚不能确认 `{grouping_variable_label}` 会稳定影响 `{outcome_label}`。因此，不建议仅根据当前分析结果立即调整方案或资源投入。更合适的做法是扩大样本、优化测量指标，或结合更多行为数据进行复核。

### 3.3 存在 caution 时的行动推荐模板

由于 suitability check 显示部分统计前提存在风险，本报告已采用更合适的替代方法或保留 caution。后续工作中，建议优先检查数据质量，并通过更大样本、真实任务记录或重复试点来验证当前结果是否稳定。

### 3.4 可选行动建议列表

根据结果内容，可以选择以下建议中的若干条，不需要全部使用：

1. 选择表现较好的组别方案进入下一轮小规模试点；
2. 继续追踪任务耗时、完成质量、用户反馈、使用频率等关键指标；
3. 对效果不明显的方案进行功能拆解，判断问题来自工具能力不足、使用门槛过高，还是任务场景不匹配；
4. 在扩大推广前，进行更长周期或更贴近真实工作的验证；
5. 将统计结果与实施成本、用户接受度和业务目标结合判断，而不是只根据显著性作决策；
6. 如果结果不稳定，优先检查样本量、测量指标和数据质量，再决定是否调整方案；
7. 如果组间差异集中在某一类结果指标上，后续优化应优先围绕该指标展开；
8. 如果某方案在效果提升和成本控制之间更平衡，可以将其作为优先迭代方向。

## 5. 写作规则

1. 报告主体使用中文。
2. 报告开头必须先给“核心内容”，不要一开始堆统计值。
3. 报告主体分为两部分：核心内容、详细统计报告。
4. 核心内容下必须有 `1.1 报告目标`、`1.2 核心结果`、`1.3 行动建议`。
5. 图放在核心结果附近，不单独创建图的小节。
4. 第一版只放一张合并图，展示三个 outcome 的组间分布与均值趋势。
5. 第一版只放一个均值表，使用 `M_subscript (SD)` 和字母下标说明组间显著差异。
6. 主效应结果用正文 APA-style 报告，不需要单独生成 ANOVA summary table。
7. 不需要单独生成完整 pairwise comparison table，pairwise 结果用于生成正文说明、显著性 brackets 和字母下标。
8. 统计符号和 APA 格式保留标准写法，例如 `F(3, 196) = 8.42, p < .001, η² = .11`。
9. Word 中非罗马统计符号和统计缩写需斜体，包括 `F`, `p`, `η²`, `M`, `SD`, `ps`。
10. 每个结果先解释实际含义，再报告统计值。
11. 行动推荐必须说明当前结果如何服务于未来的工作调整，例如试点、资源投入、流程优化、后续验证或指标追踪。
12. 行动推荐部分不要出现“如果这是实际业务数据”“如果该结果来自真实业务数据”等表达。
13. 正式业务报告正文不写 synthetic/mock data 开头说明；公开展示限制说明保留在项目文档中。
14. 避免使用过度学术化表达，例如“为完整性起见”“预先设定的对比”“常规显著性水平”“潜变量层面的稳健性检验”等，除非用户明确要求学术论文风格。
15. 不要把 synthetic/mock data 描述成真实证据。
16. 不要过度声称因果关系，除非 analysis plan 明确说明数据来自实验设计。
17. 如果 suitability check 显示 caution，需要在报告中保留提醒。
18. 如果 decision 是 `diagnostic_only` 或 `stop_analysis`，不要生成正式推断性结论。
19. 正文、图示、均值表和 quality check 必须保持一致。
20. 图用于讲趋势，表用于讲各组均值和组间差异。
21. 报告应让非统计背景的面试官能够理解，同时保留必要的统计严谨性。
22. 第一版 Word 报告应控制图表数量，避免过度学术化。
23. Word 正文段落首行缩进两个中文字。
24. 表格宽度尽量填满页面，单元格内容垂直居中。
25. 一级 section 之间应保留明确视觉间距。
26. 百分比解释应融入核心结论段落，不单独作为机械短段。
27. 图表标题、内容和注释应作为一个整体 block 处理，留白加在 block 前后。

## 6. 当前项目固定偏好

- 三个因变量都运行并展示结果。
- 三个因变量放在同一张 manuscript-ready 组合图中。
- 图形参考 raincloud 风格：jittered points、boxplots、half-violins 和显著性 brackets。
- 只生成一个均值表，表格使用 compact letter display 标注组间显著性。
- human review decision 应按 outcome 单独确认。
- 若与旧 skill 或旧模板存在冲突，以当前项目对话中确认的业务友好报告标准为准。
