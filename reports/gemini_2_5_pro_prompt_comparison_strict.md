# EmotionBench Gemini 2.5 Pro 严格格式复盘报告

## 说明

- 这份报告不是新的云端 rerun，而是对现有 `baseline_20` 与 `cot_20` 结果做严格格式复盘。
- 由于当前代理配额不足，20 条真实 rerun 被 403 quota 拒绝，因此论文里应以这份严格复盘为准，并在方法部分注明“格式合规率”指标。

## 对比表

| Metric | Baseline | CoT | Delta (CoT - Baseline) |
|---|---:|---:|---:|
| Accuracy | 50.00% | 25.00% | -25.00pp |
| Strict Accuracy | 10.00% | 0.00% | -10.00pp |
| Macro-F1 | 37.50% | 13.33% | -24.17pp |
| Format Valid Rate | 10.00% | 0.00% | -10.00pp |
| Invalid Output Count | 18 | 20 | 2 |
| Normal | 75.00% | 0.00% | -75.00pp |
| Sarcasm | 50.00% | 33.33% | -16.67pp |
| Metaphor | 50.00% | 33.33% | -16.67pp |
| Adversarial | 25.00% | 25.00% | +0.00pp |
| Robustness | 0.00% | 0.00% | +0.00pp |

## 关键观察

- Baseline 的 format_valid_rate 只有 10.00%，说明 20 条里只有少数输出是严格标签格式。
- CoT 的 format_valid_rate 为 0.00%，说明它几乎完全没有给出合格标签。
- Baseline 的 strict_accuracy 为 10.00%，CoT 的 strict_accuracy 为 0.00%。
- 因此，原始 accuracy 不能单独看，必须和严格格式合规率一起报告。

## 结论

- 这次结果不是“模型真的全答错”，而是**大量输出格式不合规**，导致原始 accuracy 被格式噪声污染。
- 以后论文和后续实验都应使用 Level 1 / Level 2 的统一规范，并强制记录 `format_valid_rate` 与 `strict_accuracy`。
- 由于当前云端额度不足，20 条同模型 rerun 暂时无法完成，需要补充额度或切换更便宜模型后再做正式重跑。
