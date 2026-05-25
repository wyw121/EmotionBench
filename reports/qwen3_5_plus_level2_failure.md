# qwen3.5-plus Level 2 失败记录

- 模型：`qwen3.5-plus`
- 等级：Level 2（101 条）
- 运行入口：`scripts/run_real_model_benchmark.py`
- 当前失败类型：`openai.APIConnectionError` / `httpx.RemoteProtocolError`
- 错误摘要：`Server disconnected without sending a response.`
- 已尝试重试：3 次
- 结论：这次失败属于上游兼容接口连接不稳定，不是评测脚本语法错误
- 处理建议：稍后重试，或更换更稳定的兼容接口/模型实例
