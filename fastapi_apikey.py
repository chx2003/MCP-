from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict

app = FastAPI()

# 模拟的用户数据库：{api_key: user_info}
# 使用类似真实的API Key（随机字符串，字母+数字+特殊字符）
# 在实际应用中，应使用数据库（如SQL数据库）并确保API Key安全存储
USERS_DB: Dict[str, Dict] = {
    "sk-7b9f2a4c9e3d8f1b6c0e2a8d4f5e9c3b1a7f8e2d": {"user_id": "user1", "username": "Alice"},
    "sk-4e8c1b3f6a2d9e7f0c5b3a1e8d2f6c9b4a0e7f3c": {"user_id": "user2", "username": "Bob"},
}

# 定义Bearer令牌验证方式
security = HTTPBearer()

# 验证API Key并返回用户信息
async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    
    api_key = credentials.credentials
    if api_key not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    
    return USERS_DB[api_key]

# 简单的GET接口，返回用户信息
@app.get("/hello")
async def read_hello(current_user: Dict = Depends(verify_api_key)):
    return {
        "message": f"Hello, {current_user['username']}!",
        "user_id": current_user['user_id']
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# 请求示例
"""

 curl -X GET "http://localhost:8000/hello"  -H "Authorization: Bearer sk-7b9f2a4c9e3d8f1b6c0e2a8d4f5e9c3b1a7f8e2d"

"""



