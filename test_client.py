from fastmcp import Client
from fastmcp.client.transports import (PythonStdioTransport, SSETransport)
import asyncio
 
async def mytest():
     async with Client(PythonStdioTransport("/Users/denggao/codeBase/mcp_demos/weather_service.py")) as client:         
        result = await client.call_tool("get_current_weather", {"province": "北京", "city": "海淀"})
        return result

async def test_resource():
     async with Client(PythonStdioTransport("/Users/denggao/codeBase/mcp_demos/weather_service.py")) as client:         
        result = await client.read_resource("greeting://denggao")
        print("test_resource: " ,result)
        text = result[0].text
        return text 

async def test_resource_prompt():
     async with Client(PythonStdioTransport("/Users/denggao/codeBase/mcp_demos/weather_service.py")) as client:         
        result = await client.get_prompt("ask_review", {"code_snippet": " print('hello') "} )
        print("test_resource_prompt: " ,result[0].content.text)
        return result 

async def test_list():
     async with Client(PythonStdioTransport("/Users/denggao/codeBase/mcp_demos/weather_service.py")) as client:         
        tools = await client.list_tools()
        resources = await client.list_resources()
        #print("tools: " ,tools)
        print("resources: " ,resources)
        #return tools, resources


async def test_sse():
     async with Client(SSETransport("http://127.0.0.1:8888/sse")) as client: 
        tools = await client.list_tools()   
        print("tools: " ,tools)     
        result = await client.call_tool("get_current_weather", {"province": "北京", "city": "海淀"})
        return result


async def test_es_sse():
     async with Client(SSETransport("http://127.0.0.1:9005/sse")) as client: 
        tools = await client.list_tools()   
        print("tools: " ,tools)     
        result = await client.call_tool("perform_elastic_search", {"query": "哥哥"})
        return result

if __name__ == "__main__":
    # result = asyncio.run(mytest())
    # print(result)

    # result2 = asyncio.run(test_resource())
    # print(result2)

    # result3 = asyncio.run(test_resource_prompt())
    # print(result3)

    # result4 = asyncio.run(test_list())
    # print(result4)

    result5 = asyncio.run(test_es_sse())
    print(result5)