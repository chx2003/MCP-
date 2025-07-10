from fastmcp import FastMCP
import sqlite3

# 数据库连接
conn = sqlite3.connect('chat_history.db')
cursor = conn.cursor()

# 创建 FastMCP 服务器
mcp = FastMCP("order service mcp", host="127.0.0.1", port=9002 )


@mcp.tool(description="获取指定月份的销售总额")
def get_monthly_sales_total(month: int) -> str:
    # 验证月份参数
    if not (1 <= month <= 12):
        return "无效的月份"
    
    # 将整数月份转换为两位数字字符串（如 1 -> '01'）
    month_str = f"{month:02d}"
    
    # 参数化查询
    query = """
    SELECT SUM(price) as total_sales
    FROM orders
    WHERE strftime('%m', datetime(create_time, 'unixepoch')) = ?
    """
    cursor.execute(query, (month_str,))
    result = cursor.fetchone()
    
    # 处理查询结果
    if result[0] is None:
        return f"{month}月没有销售记录"
    return f"{month}月的销售总额：{result[0]}"
 

@mcp.tool(description="获取消费最高的用户")
def get_highest_spending_customer() -> str:
    query = """
    SELECT customer_name, SUM(price) as total_consumption
    FROM orders
    GROUP BY customer_name
    ORDER BY total_consumption DESC
    LIMIT 1
    """
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return "未找到客户记录"
    return f"消费最高的用户：{result[0]}，总消费额 {result[1]}"

# 工具 3：获取最受欢迎的产品（基于订单数量）
@mcp.tool(description="获取最受欢迎的产品（基于订单数量）")
def get_most_popular_product() -> str:
    query = """
    SELECT product_name, COUNT(*) as order_count
    FROM orders
    GROUP BY product_name
    ORDER BY order_count DESC
    LIMIT 1
    """
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return "未找到产品记录"
    return f"最受欢迎的产品：{result[0]}，订单数量 {result[1]}"

# 工具 4：获取销售员排行榜（基于总销售额）
@mcp.tool(description="获取销售员排行榜（基于总销售额）")
def get_salesperson_ranking(limit: int = 10) -> str:
    query = f"""
    SELECT sales_name, SUM(price) as total_sales
    FROM orders
    GROUP BY sales_name
    ORDER BY total_sales DESC
    LIMIT ?
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    if not results:
        return "未找到销售员记录"
    ranking = "销售员排行榜：\n" + "\n".join([f"{name}: {sales}" for name, sales in results])
    return ranking

# 运行 FastMCP 服务器
if __name__ == "__main__":
    mcp.run( transport="sse")