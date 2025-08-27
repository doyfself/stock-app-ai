import requests
import time
import datetime


def read_cookie_from_file(file_path="cookie.txt"):
    """从文件读取cookie"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def parse_stock_data(raw_data):
    """将原始数据转换为目标格式"""
    result = []
    # 提取column和item数据
    columns = raw_data.get("data", {}).get("column", [])
    items = raw_data.get("data", {}).get("item", [])

    for item in items:
        # 创建映射关系（column索引 -> 目标字段）
        data_map = dict(zip(columns, item))

        # 转换时间戳为YYYY-MM-DD格式
        timestamp = data_map.get("timestamp")
        if timestamp:
            dt = datetime.datetime.fromtimestamp(timestamp / 1000)
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        else:
            date_str = ""

        # 组装目标格式数据
        result.append(
            {
                "date": date_str,
                "open": data_map.get("open") or 0,  # 处理null值
                "high": data_map.get("high") or 0,
                "low": data_map.get("low") or 0,
                "close": data_map.get("close") or 0,
                "volume": data_map.get("volume") or 0,
                "percent": data_map.get("percent") or 0,
                "turnoverrate": data_map.get("turnoverrate") or 0,
            }
        )
    return result


def get_headers():
    # 读取cookie
    cookie = read_cookie_from_file()
    if not cookie:
        return {"success": False, "count": 0, "data": [], "message": "cookie文件不存在"}

    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://xueqiu.com/",
        "Cookie": cookie,
    }
    return headers


def get_stock_data(params):
    # 构建请求参数
    code = params.get("code", [""])[0].strip().upper()
    period = params.get("period", ["daily"])[0].strip().lower()
    timestamp = params.get("timestamp", [""])[0].strip().lower()
    limit = params.get("limit", [100])[0].strip().lower()

    # 获取当前时间戳（毫秒）并延后一天
    if timestamp == "":
        # 计算一天的毫秒数：24*60*60*1000 = 86400000
        ONE_DAY_MS = 86400 * 1000
        current_timestamp = int(time.time() * 1000)
        timestamp = current_timestamp + ONE_DAY_MS
    url = f"https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={code}&begin={timestamp}&period={period}&type=before&count=-{limit}&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"

    print(url)
    headers = get_headers()
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        print(f"请求URL: {url}")  # 调试输出
        response.raise_for_status()  # 触发HTTP错误
        raw_data = response.json()

        # 检查数据是否为空
        items = raw_data.get("data", {}).get("item", [])
        if not items:
            return {"success": False, "count": 0, "data": [], "message": "cookie已过期"}

        # 解析数据
        parsed_data = parse_stock_data(raw_data)

        # 返回成功响应
        return {
            "success": True,
            "count": len(parsed_data),
            "data": parsed_data,
            "message": f"成功获取{len(parsed_data)}条数据",
        }

    except requests.exceptions.HTTPError as e:
        # 处理HTTP错误（如403、401等）
        return {"success": False, "count": 0, "data": [], "message": "cookie已过期"}
    except Exception as e:
        # 处理其他异常
        return {
            "success": False,
            "count": 0,
            "data": [],
            "message": f"请求失败：{str(e)}",
        }


def get_selection_details(params):
    symbols = params.get("symbols", [""])[0].strip().upper()
    url = f"https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol={symbols}"

    headers = get_headers()
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 触发HTTP错误
        raw_data = response.json()

        # 检查数据是否为空
        items = raw_data.get("data", {}).get("items", {})
        if not items:
            return {"success": False, "count": 0, "data": [], "message": "cookie已过期"}

        # 返回成功响应
        return {
            "success": True,
            "data": [item.get("quote") for item in items if item.get("quote")],
            "message": "成功获取",
        }

    except Exception as e:
        # 处理其他异常
        return {
            "success": False,
            "count": 0,
            "data": {},
            "message": f"请求失败：{str(e)}",
        }


def get_stock_details(params):
    # 构建请求参数
    code = params.get("code", [""])[0].strip().upper()
    url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={code}&extend=detail"

    headers = get_headers()
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        print(f"请求URL: {url}")  # 调试输出
        response.raise_for_status()  # 触发HTTP错误
        raw_data = response.json()

        # 检查数据是否为空
        items = raw_data.get("data", {}).get("quote", {})
        if not items:
            return {"success": False, "count": 0, "data": [], "message": "cookie已过期"}

        # 返回成功响应
        return {"success": True, "data": items, "message": "成功获取"}

    except requests.exceptions.HTTPError as e:
        # 处理HTTP错误（如403、401等）
        return {"success": False, "count": 0, "data": {}, "message": "cookie已过期"}
    except Exception as e:
        # 处理其他异常
        return {
            "success": False,
            "count": 0,
            "data": {},
            "message": f"请求失败：{str(e)}",
        }
