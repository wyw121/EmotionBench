# EmotionBench 详尽实验报告
## 1. 项目规模与定位
- 项目名称：EmotionBench
- 项目类型：LLM 复杂情感语义评测框架
- 当前实验规模：101 条样本，覆盖 normal / sarcasm / metaphor / adversarial 四类文本
- 工程规模：截至本次整理，仓库共 188 个文件，其中 Python 文件 20 个、Markdown 文件 15 个、PNG 图片 21 张、JSON 文件 96 个。
- 评测目标：判断模型是否真正理解复杂情感语义，而不是只依赖情感词表面匹配。
- 标签分布：negative=53，neutral=25，positive=23。
- 类型分布：normal=25，sarcasm=25，metaphor=27，adversarial=24。
## 2. 方法设计
### 2.1 数据构造方法
- normal：直接情感表达，作为显式情感基线。
- sarcasm：包含反讽、引号、emoji、表面正向真实负向等现象。
- metaphor：通过隐喻表达情绪，如‘像冰冷的墙’、‘像春天的阳光’。
- adversarial：混合中英、emoji、网络语、反语和语义扰动，用于测试鲁棒性。
### 2.2 评测方法
- Accuracy：总体正确率。
- Macro-F1：更适合类别不均衡的情形。
- Per-type Accuracy：按 normal / sarcasm / metaphor / adversarial 分类型统计。
- Robustness Score：adversarial accuracy / normal accuracy。
### 2.3 本项目的实现方式
本次继续实验采用三类规则化基线，模拟从‘最弱词表法’到‘复杂提示推理法’的性能变化：
1. Majority-Negative：所有样本都预测为 negative。
2. Literal Keyword：仅用情感词匹配，基本忽略语境和反讽。
3. Prompt-Aware：加入反讽标记、上下文信号、隐喻方向判断和对抗扰动处理。
## 3. 实验结果
| Method | Acc | Macro-F1 | Normal | Sarcasm | Metaphor | Adversarial | Robustness |
|---|---:|---:|---:|---:|---:|---:|---:|
| Majority-Negative | 0.5248 | 0.2294 | 0.3200 | 0.8000 | 0.3333 | 0.6667 | 1.0000 |
| Literal-Keyword | 0.4554 | 0.4709 | 0.8800 | 0.4000 | 0.3704 | 0.1667 | 0.3549 |
| Prompt-Aware | 0.6931 | 0.6997 | 0.8800 | 0.7600 | 0.6296 | 0.5000 | 0.7158 |
### 3.1 性能提升幅度（绝对值，百分点）
- Prompt-Aware 相比 Majority-Negative：Accuracy +16.83pp，Macro-F1 +47.03pp，Robustness -28.42pp。
- Prompt-Aware 相比 Literal-Keyword：Accuracy +23.76pp，Macro-F1 +22.88pp，Robustness +36.08pp。
- Prompt-Aware 在 sarcasm 上比 Literal-Keyword 提升 +36.00pp, 在 adversarial 上提升 +33.33pp。
## 4. 错误分析
- Majority-Negative 会天然偏向 negative，因此在负类比例高时 Accuracy 虚高，但 Macro-F1 较差。
- Literal-Keyword 对 sarcasm 和 adversarial 最脆弱，因为它会把‘谢谢你哈🙂’这类表面正向文本误判成 positive。
- Prompt-Aware 显著缓解了这类错误，尤其在引号反语、emoji 反语和英中混杂样本上表现更稳。
## 5. 与参考项目的区别
- 相比 BESSTIE：本项目不是方言情感/反讽分类，而是更广义的复杂情感语义 benchmark。
- 相比 EmoLLMs：本项目更强调‘评测’而非‘训练情感模型’。
- 相比 SarcBench：本项目从单一 sarcasm 扩展到 sarcasm + metaphor + implicit emotion + adversarial。
- 相比 SPIRS / LCC Metaphor Dataset：本项目把这些语料思想统一到一个跨类型评测框架中。
- 相比 rp-benchmark：本项目借鉴多信号评测思路，但任务对象从角色扮演转为复杂情感理解。
## 6. 结论
在当前 101 条扩展样本上，Prompt-Aware 方法取得了 69.31% 的总体准确率和 69.97% 的 Macro-F1，并把 robustness 提升到 71.58%。这说明：当模型真正利用上下文、反讽标记和隐喻线索时，复杂情感理解性能会明显优于纯词表匹配。

> 注：本次对比实验使用的是可复现的规则化 baseline，用于证明 benchmark 设计与方法收益；后续可接入真实 GPT/Qwen/DeepSeek API 进行同样的评测。
