import csv
import os
from datetime import datetime
from typing import Dict, List, Optional

# 基础配置
MARKET_ANALYSIS_DIR = "marketAnalysis"  # 分析文件存放目录
CSV_HEADERS = ["date", "analysis"]  # 分析文件表头
DATE_FORMAT = "%Y-%m-%d"  # 日期格式


def ensure_directory_exists() -> None:
    """确保市场分析目录存在，不存在则创建"""
    if not os.path.exists(MARKET_ANALYSIS_DIR):
        os.makedirs(MARKET_ANALYSIS_DIR)


def get_csv_path(code: str) -> str:
    """根据股票代码获取对应的CSV文件路径"""
    ensure_directory_exists()
    return os.path.join(MARKET_ANALYSIS_DIR, f"{code.strip().upper()}.csv")


def init_csv_file(code: str) -> None:
    """初始化指定股票代码的CSV文件（不存在则创建并写入表头）"""
    csv_path = get_csv_path(code)
    if not os.path.exists(csv_path):
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()


def get_analysis_info(params: Optional[Dict] = None) -> Dict:
    """
    获取分析信息接口
    接收参数code，多个code以逗号隔开
    返回每个code对应的CSV文件最后一条数据
    """
    # 参数校验
    if not params or "code" not in params:
        return {"success": False, "message": "缺少code参数"}, 400

    # 处理code参数（兼容列表/字符串类型）
    code_param = params["code"]
    code_str = (
        code_param[0].strip()
        if isinstance(code_param, list)
        else str(code_param).strip()
    )

    if not code_str:
        return {"success": False, "message": "code参数不能为空"}, 400

    # 分割多个code
    codes = [code.strip().upper() for code in code_str.split(",") if code.strip()]
    if not codes:
        return {"success": False, "message": "未提供有效的code"}, 400

    result = {"success": True, "data": {}, "message": "获取分析信息成功"}

    try:
        for code in codes:
            csv_path = get_csv_path(code)
            # 确保文件存在
            init_csv_file(code)

            last_analysis = None
            with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                # 读取所有行并获取最后一行
                rows = list(reader)
                if rows:
                    last_analysis = rows[-1]

            result["data"][code] = last_analysis

        return result
    except Exception as e:
        return {"success": False, "message": f"获取分析信息失败: {str(e)}"}, 500


def add_analysis_info(_, request_body: Dict) -> Dict:
    """
    新增分析信息接口
    接收code和analysis参数，POST请求
    自动获取当日日期，格式为年-月-日
    若当天已有分析，则替换；否则新增
    """
    # 参数校验
    if "code" not in request_body or "analysis" not in request_body:
        return {"success": False, "message": "缺少code或analysis参数"}, 400

    code = request_body["code"].strip().upper()
    analysis = request_body["analysis"].strip()

    if not code:
        return {"success": False, "message": "code参数不能为空"}, 400

    if not analysis:
        return {"success": False, "message": "analysis参数不能为空"}, 400

    # 获取当日日期
    today = datetime.now().strftime(DATE_FORMAT)

    try:
        csv_path = get_csv_path(code)
        init_csv_file(code)  # 确保文件存在
        rows: List[Dict] = []
        today_exists = False

        # 读取现有数据
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 如果找到今天的记录，标记并替换
                if row["date"] == today:
                    rows.append({"date": today, "analysis": analysis})
                    today_exists = True
                else:
                    rows.append(row)

        # 如果今天没有记录，添加新记录
        if not today_exists:
            rows.append({"date": today, "analysis": analysis})

        # 写回所有数据
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {
            "success": True,
            "data": {"code": code, "date": today, "analysis": analysis},
            "message": f"{'更新' if today_exists else '新增'}股票{code}的分析信息成功",
        }
    except Exception as e:
        return {"success": False, "message": f"操作失败: {str(e)}"}, 500
