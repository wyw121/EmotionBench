# EmotionBench Prompt 对比结果

## 实验设置

- Model: `[芝士]gemini-2.5-pro`

- Provider: `OpenRouter`

- Dataset size: `20`

- Baseline prompt: `baseline.txt`

- CoT prompt: `cot_prompt.txt`

- Shuffle: fixed seed, same sample order

- Temperature: 0


## 对比表

| Metric | Baseline | CoT | Delta (CoT - Baseline) |
|---|---:|---:|---:|
| Accuracy | 50.00% | 25.00% | -25.00pp |
| Macro-F1 | 37.50% | 13.33% | -24.17pp |
| Normal | 75.00% | 0.00% | -75.00pp |
| Sarcasm | 50.00% | 33.33% | -16.67pp |
| Metaphor | 50.00% | 33.33% | -16.67pp |
| Adversarial | 41.67% | 30.56% | -11.11pp |
| Robustness | 55.56% | 0.00% | -55.56pp |

## 结论

- Accuracy delta: -25.00pp

- Macro-F1 delta: -24.17pp

- Robustness delta: -55.56pp
