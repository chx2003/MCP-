# MCP-进阶



## 参考资料

**MCP协议官方网站**
https://modelcontextprotocol.io/specification/2025-03-26/server/tools

## 安装依赖

建议使用虚拟环境。依赖已在 `requirements.txt` 中列出，安装命令如下：

```bash
pip install -r requirements.txt
```

## 主要脚本说明

1. `weather_server.py`：用 SSE 方式提供天气查询，启动命令 `python weather_server.py`，供远程调用。
2. `weather_stdio.py`：功能同上，用标准输入输出通信，适合被其他脚本通过管道调用，启动命令 `python weather_stdio.py`。
3. `order_server.py`：基于本地数据库做订单分析（算销售额、找大客户等），启动命令 `python order_server.py`，供外部调用。
4. `poem_server.py`：用大模型 API 生成指定主题的诗歌，启动命令 `python poem_server.py`，可生成诗歌或摘要。
5. `poem_client.py`：演示怎么调用上面的诗歌服务，启动命令 `python poem_client.py`，是客户端示例。
6. `test_sse.py`：测试 SSE 通信（连服务器、拿工具列表等），启动命令 `python test_sse.py`，用于测试 SSE 协议。
7. `test_client.py`：演示客户端用 SSE 和 Stdio 两种方式调用服务，启动命令 `python test_client.py`，是客户端测试脚本。
8. `test_stdio.py`：通过管道和 `weather_stdio.py` 通信，发消息看回复，启动命令 `python test_stdio.py`，用于测试 Stdio 协议。
9. `fastapi_mcp_server.py`：把 FastAPI 和 FastMCP 放一起用，支持网页场景，启动命令 `python fastapi_mcp_server.py`，是 Web 服务示例。
10. `es_mcp_server.py`：结合 Elasticsearch 提供全文搜索，能搜指定内容并高亮，启动命令 `python es_mcp_server.py`，供检索用。
11. `fastapi_apikey.py`：用 FastAPI 做了个 API 密钥认证示例，能保护接口，启动命令 `python fastapi_apikey.py`，适合需要安全认证的场景。

---

如需详细用法或扩展开发，请参考各脚本内注释和 FastMCP 官方文档。
