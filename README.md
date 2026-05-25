# EmotionBench: Evaluating LLMs on Complex Emotional Semantics

EmotionBench 是一个面向课程论文的 LLM 复杂情感理解评测框架，重点评估模型是否真正理解：

- 反讽（sarcasm）
- 隐喻（metaphor）
- 隐式情感（implicit emotion）
- 对抗文本（adversarial samples）

## 项目目标

这个项目将“论文方法设计”和“代码实验框架”统一起来，支持：

- 数据集构建与加载
- Prompt 设计与对比实验
- 评测指标统计
- 鲁棒性分析
- 图表可视化
- 错误案例导出

## 论文参考脉络

本项目参考了以下研究/资源的思路：

- `CULEMO`：跨文化情感理解基准，强调情感语义不只依赖关键词，而依赖上下文和文化推理。
- `AI with Emotions`：通过指定情绪状态观察 LLM 的情绪表达能力。
- `BESSTIE`：情感与反讽双任务评测，启发了本项目的双层标签设计。
- `EmoLLMs`：情绪强度、情感分类的提示词模板，启发了本项目的 prompt 组织方式。
- `SarcBench`：上下文驱动的反讽理解多选评测，启发了本项目的对抗问答设计。
- `SPIRS` 与隐喻数据集：启发了“真实上下文 + 语义反转 + 隐含情绪”的样本构造思路。
- `rp-benchmark`：启发了“多信号评测 + 仪表盘 + 错误分析”的工程组织方式。

## 目录结构

```text
EmotionBench/
├── dataset/
├── prompts/
├── evaluation/
├── visualization/
├── results/
├── src/
└── main.py
```

## 快速开始

1. 安装依赖

```bash
pip install -r requirements.txt
```

1. 生成示例数据

```bash
python main.py build-dataset --output dataset
```

1. 评测一个结果文件

```bash
python main.py evaluate --predictions results/demo_predictions.json
```

1. 导出图表

```bash
python main.py visualize --predictions results/demo_predictions.json --output results/charts
```

## 真实模型接入

如果你要跑 GPT / Qwen / DeepSeek / SiliconFlow 的真实结果表，需要准备 API Key。当前仓库已提供：

- `.env.example`：环境变量模板
- `.env`：本地私密配置文件（不要提交到 Git）
- `scripts/run_real_model_benchmark.py`：统一跑真实模型的脚本
- `scripts/run_model_level_suite.py`：按 Level 0 / 1 / 2 批量跑模型的脚本

### 运行方式

先编辑 `.env`，填入对应平台的 Key 和模型名，然后运行：

```bash
python scripts/run_real_model_benchmark.py --provider gpt --dataset dataset_expanded --prompt baseline.txt --limit 20
python scripts/run_real_model_benchmark.py --provider qwen --dataset dataset_expanded --prompt baseline.txt --limit 20
python scripts/run_real_model_benchmark.py --provider deepseek --dataset dataset_expanded --prompt baseline.txt --limit 20
python scripts/run_real_model_benchmark.py --provider siliconflow --model deepseek-ai/DeepSeek-V4-Flash --dataset dataset_expanded --prompt baseline.txt --limit 10
```

### 成本说明

是的，**真实调用通常是要钱的**。费用主要来自：

- 输入 token
- 输出 token
- 模型档位（mini / standard / pro）

建议先用 `--limit 10` 或 `--limit 20` 做 smoke test，确认 prompt、解析和保存结果都没问题，再扩大到全量。

### 省钱建议

- 先跑小样本验证流程
- 优先使用便宜的轻量模型做 baseline
- 同一套 prompt 只改 provider，避免重复开发
- 如果要严格比较，固定 temperature=0

### Gemini 反代 / 兼容接口

如果你买的是第三方反代或 OpenAI-compatible 接口，可以走通用模式：

1. 把密钥写入本地 `.env`，不要发到聊天里。
1. 配置下面三个字段：

```bash
COMPATIBLE_API_KEY=你的密钥
COMPATIBLE_BASE_URL=https://cheeseapi.top/v1
COMPATIBLE_MODEL=你账号对应的 Gemini 模型名
```

1. 用通用 provider 跑：

```bash
python scripts/run_real_model_benchmark.py --provider compatible --dataset dataset_expanded --prompt baseline.txt --limit 20 --shuffle
```

### SiliconFlow 批量测试

如果你要系统测试多个 SiliconFlow 模型，可以先在 `.env` 中填写：

```bash
SILICONFLOW_API_KEY=你的密钥
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
```

然后使用批跑脚本：

```bash
python scripts/run_model_level_suite.py --provider siliconflow --models deepseek-ai/DeepSeek-V4-Flash Pro/moonshotai/Kimi-K2.6 Pro/zai-org/GLM-5.1 MiniMaxAI/MiniMax-M2.5 Qwen/Qwen3.6-35B-A3B --levels 0 1 2
```

默认规则：

- Level 0：10 条 smoke test
- Level 1：20 条 diagnostic test
- Level 2：101 条 paper-scale benchmark

每个模型都会输出到 `results/runs/<provider>/<model>/level<level>_<label>/`。

### 安全提醒

- 你刚贴出来的密钥应视为已经泄露，建议立刻作废或轮换。
- 第三方“尝鲜卡 / 反代”服务稳定性和合规性都不如官方渠道，适合做短期测试，不建议作为长期论文主方案。

## 评估规模规范

为了让后续所有模型 API 都输出统一结构，本项目把实验分成 4 个等级：

- Level 0：10 条 smoke test
- Level 1：20 条 diagnostic test
- Level 2：101 条 paper-scale benchmark
- Level 3：200+ 条 extended benchmark

正式论文结果优先使用 Level 2；prompt 对比可以先用 Level 1。

规范说明见 `reports/evaluation_scale_spec.md`。

## 数据格式

每条样本使用统一 JSON 格式：

```json
{
  "id": "sarcasm_001",
  "text": "谢谢你哈🙂，让我等了两个小时。",
  "label": "negative",
  "type": "sarcasm",
  "difficulty": "medium",
  "context": "用户抱怨客服响应太慢"
}
```

## 结果格式

模型预测结果文件支持两种形式：

### 形式 1：直接预测标签

```json
[
  {
    "id": "sarcasm_001",
    "prediction": "negative"
  }
]
```

### 形式 2：包含原始回答

```json
[
  {
    "id": "sarcasm_001",
    "prediction": "negative",
    "raw_output": "The tone is negative because..."
  }
]
```

## 评测指标

- Accuracy
- Macro-F1
- Per-type Accuracy
- Robustness Score
- Confusion Matrix

## 课程论文对应建议

- 第一章：研究背景与问题定义
- 第二章：相关工作
- 第三章：数据集与方法设计
- 第四章：实验设置与评测指标
- 第五章：结果分析与错误案例
- 第六章：总结与展望

## 说明

当前仓库提供的是一个可扩展的研究框架，后续可接入 GPT、Qwen、DeepSeek 等 API，或者直接导入你手工整理的实验结果。
