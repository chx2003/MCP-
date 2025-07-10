import subprocess
import json


# 4条JSON-RPC消息
messages = [
    {"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"sampling":{},"roots":{"listChanged":"true"}},"clientInfo":{"name":"mcp","version":"0.1.0"}}},
    {"jsonrpc":"2.0","method":"notifications/initialized"},
    {"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}},
    {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_current_weather","arguments":{"province":"北京","city":"海淀"}}}
]

def main():
    # 启动接收端脚本，通过管道通信
    process = subprocess.Popen(
        ["python", "weather_stdio.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    # 发送消息并收集响应
    responses = []
    for msg in messages:
        # 将消息序列化为JSON字符串并发送
        msg_str = json.dumps(msg) + "\n\n"
        process.stdin.write(msg_str)
        process.stdin.flush()  # 确保消息立即发送

        # 读取响应（除了通知消息外，其他消息都有响应）
        if "id" in msg:  # 只有带id的消息有响应
            response = process.stdout.readline().strip()
            if response:
                #print(f"Response : {response}")
                responses.append(response)

    # 关闭管道并等待接收端进程结束
    process.stdin.close()

    # 打印所有响应
    for i, resp in enumerate(responses, 1):
        print(f"Response {i}:   {resp}")

if __name__ == "__main__":
    main()