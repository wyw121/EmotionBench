# SiliconFlow Level 2 测试阻塞记录

- 尝试模型：`deepseek-ai/DeepSeek-V4-Flash`、`Pro/moonshotai/Kimi-K2.6`、`Pro/zai-org/GLM-5.1`、`MiniMaxAI/MiniMax-M2.5`、`Qwen/Qwen3.6-35B-A3B`、`Qwen/Qwen3-32B`
- 运行等级：Level 2（101 条）
- 运行入口：`scripts/run_model_level_suite.py`
- 当前阻塞原因：SiliconFlow 返回 `403`，错误信息为 `Sorry, your account balance is insufficient`（在 `Qwen/Qwen3-32B` 的 smoke test 中同样复现）
- 结论：不是脚本逻辑错误，而是账号余额不足，所有后续模型预计都会受同一限制影响
- 建议：补充余额后重新运行同一命令；如果想先验证流程，可临时切换到余额充足的账号或更便宜的模型