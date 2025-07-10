from fastmcp import FastMCP, Context
import requests 

# Initialize poemMCP server
mcp = FastMCP("poemMCP", dependencies=["requests"] ,  host="127.0.0.1", port=9003,   )

# 定义生成诗歌的工具
@mcp.tool(name="generate_poem", description="Generate a poem about a given topic")
async def generate_poem(context: Context , topic: str):
    poem = await context.sample(
        f"Write a short poem about {topic}",
        system_prompt="You are a talented poet." 
    )
    return poem




# 定义总结文档的工具
@mcp.tool(description="Summarize a given document")
async def summarize_document(context: Context, document: str):
    """Summarize a given document"""
    response = await context.sample(
        f"Summarize the following document: {document}",
        system_prompt="You are a helpful summarizer."
    )
    return response


if __name__ == "__main__":
    mcp.run(transport="sse")