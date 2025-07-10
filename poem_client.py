from fastmcp import Client
from openai import OpenAI
from fastmcp.client.sampling import SamplingHandler, MessageResult
from mcp.types import SamplingMessage, TextContent
from mcp.shared.context import RequestContext # For type hint
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


MODEL_NAME = os.getenv("MODEL_NAME")

ai_client = OpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = os.getenv("BASE_URL")
) 


async def my_llm_handler(messages: list[SamplingMessage], params, context: RequestContext) -> str | MessageResult:
    print(f"Server requested sampling (Request ID: {context.request_id})")
    # In a real scenario, call your LLM API here
    last_user_message = next((m for m in reversed(messages) if m.role == 'user'), None)
    prompt = last_user_message.content.text if last_user_message and isinstance(last_user_message.content, TextContent) else "Default prompt"
    response =  ai_client.chat.completions.create(
        model = MODEL_NAME ,
        messages = messages,
        # max_tokens=params.max_tokens,  # 最大令牌数
        # temperature=params.temperature,  # 温度参数
        # top_p=params.top_p if hasattr(params, 'top_p') else 1.0  # 可选参数
    )
    # Simulate LLM response
    return response.choices[0].message.content  # 返回生成的文本


# 主函数，演示客户端如何调用服务器上的工具
async def main():
    # 创建客户端，连接到运行中的 MCP 服务器
    async with Client( "http://localhost:9003/sse", sampling_handler = my_llm_handler) as client:
        # 调用服务器上的 generate_poem 工具
        poem = await client.call_tool("generate_poem", {"topic": "hope的中文诗歌"})
        print("Generated Poem:")
        print(poem)
        print(poem[0].text)
        
        # 调用服务器上的 summarize_document 工具
        summary = await client.call_tool("summarize_document", {"document": "一副飞行员眼镜，一顶皮革飞行帽……这些是曾参与中国人民抗日战争的苏联志愿飞行员尼古拉·马特维耶夫的遗物。在莫斯科，他的孙子安德烈向中国日报记者彭译萱讲述了这些物品背后的故事。1938年，尼古拉作为苏联志愿航空队的飞行员来到中国。当他在武汉上空浴血奋战时，他的儿子在莫斯科出生，而他却将生命永远留在了中国。安德烈说，当时被派去的都是最好的飞行员，“因为当我们的朋友需要帮助时，我们就会去帮助朋友。"})
        print("Summary:")
        print(summary)
        

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())