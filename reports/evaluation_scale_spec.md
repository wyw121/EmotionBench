# EmotionBench 模型评估规模规范

## 目的

为了让后续接入的所有模型 API 都以同一结构产出结果，避免实验记录混乱，EmotionBench 采用统一的评估规模规范。

## 数据规模分级

### Level 0 - Smoke Test

- 样本量：10 条
- 目的：验证 API、prompt、解析、结果落盘是否正常
- 适用：新模型接入、接口联通测试

### Level 1 - Diagnostic Test

- 样本量：20 条
- 目的：比较 prompt 方案、检查模型在 sarcasm / metaphor / adversarial 上的基本表现
- 适用：baseline vs CoT、prompt ablation

### Level 2 - Paper-Scale Benchmark

- 样本量：101 条
- 数据来源：`dataset_expanded/all.json`
- 类型覆盖：normal / sarcasm / metaphor / adversarial
- 目的：用于论文正文中的正式结果表

### Level 3 - Extended Benchmark

- 样本量：200+ 条
- 目的：在后续扩展更多样本、更多 adversarial 变体时使用

## 统一运行约束

所有正式实验建议固定：

- `temperature=0`
- `max_tokens=64`
- `seed=42`
- 同一数据集版本
- 同一 prompt 模板
- 同一评测脚本

## 统一输出结构

每次运行都应保存以下文件：

- `summary.json`
- `predictions.json`
- `manifest.json`
- `run_config.json`
- `leaderboard.csv`

## 推荐目录结构

```text
results/
└── runs/
    └── <provider>/
        └── <model>/
            └── <prompt>/
                ├── summary.json
                ├── predictions.json
                ├── manifest.json
                ├── run_config.json
                └── leaderboard.csv
```

## 论文引用建议

论文中建议优先引用 Level 2 的正式结果；Level 1 可用于展示 prompt 对比，Level 0 仅用于接口验证。
