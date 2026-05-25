# Level 2 七模型总表

## 结果概览

| 模型 | 状态 | Accuracy | Strict Accuracy | Macro-F1 | Format Valid Rate | Invalid Outputs | Robustness Score |
|---|---|---:|---:|---:|---:|---:|---:|
| deepseek-v4-flash | completed | 0.9505 | 0.9406 | 0.9524 | 0.9505 | 5 | 0.9348 |
| minimax-m2.5 | completed | 0.2475 | 0.0000 | 0.1323 | 0.0000 | 101 | 0.6858 |
| qwen3.5-plus | failed | - | - | - | - | - | - |
| glm-5.1 | completed | 0.3069 | 0.0396 | 0.2911 | 0.0396 | 97 | 0.4468 |
| gpt-5.5 | completed | 0.9703 | 0.9703 | 0.9625 | 1.0000 | 0 | 0.9610 |
| claude-sonnet-4-6 | completed | 0.9901 | 0.9901 | 0.9861 | 1.0000 | 0 | 0.9877 |
| gemini-3.1-pro-preview | completed | 0.6535 | 0.5347 | 0.6688 | 0.5446 | 46 | 0.7566 |

## 说明

- `qwen3.5-plus` 在 Level 2 过程中遇到兼容接口连接中断，已单独记录为失败。

- 其余 6 个模型均已完成 101 条测试。

- 论文写作时建议同时报告 `Accuracy`、`Strict Accuracy`、`Format Valid Rate`，避免把格式异常误算成真实能力。
