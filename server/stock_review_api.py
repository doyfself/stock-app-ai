import csv
import uuid
import os
from typing import Dict, List, Optional

# 基础配置
BASE_CSV_FILE = "stock_review_{type}.csv"  # 带类型占位符的文件名
CSV_HEADERS = ["id", "title", "code", "date", "description"]  # 通用表头


def get_csv_path(type: str) -> str:
    """根据类型获取CSV文件路径"""
    return BASE_CSV_FILE.format(type=type.lower())


def init_csv_file(type: str) -> None:
    """初始化指定类型的CSV文件（不存在则创建并写入表头）"""
    csv_path = get_csv_path(type)
    if not os.path.exists(csv_path):
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()


from typing import Optional, Dict, List  # 确保导入必要的类型注解


def get_stock_review(params: Optional[Dict] = None) -> Dict:
    """获取指定类型的股票评论列表（支持title模糊搜索）"""
    # 1. 基础参数校验（type参数必传）
    if not params or "type" not in params:
        return {"success": False, "message": "缺少type参数"}, 400

    # 2. 处理type参数（兼容列表/字符串类型）
    type_param = params["type"]
    type = (
        type_param[0].strip()
        if isinstance(type_param, list)
        else str(type_param).strip()
    )
    if not type:
        return {"success": False, "message": "type参数不能为空"}, 400

    # 3. 处理搜索关键字（可选参数，默认空字符串）
    keyword = ""
    if "keyword" in params:
        keyword_param = params["keyword"]
        # 同样兼容列表/字符串类型的参数
        keyword = (
            keyword_param[0].strip().lower()  # 转小写，支持不区分大小写搜索
            if isinstance(keyword_param, list)
            else str(keyword_param).strip().lower()
        )

    # 4. 初始化文件并获取路径
    init_csv_file(type)
    csv_path = get_csv_path(type)
    reviews: List[Dict] = []

    try:
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 5. 模糊匹配逻辑：如果有keyword，则筛选title包含关键字的项
                if keyword:
                    # 将title转小写后判断是否包含关键字（不区分大小写）
                    if keyword in row["title"].strip().lower():
                        reviews.append(
                            {
                                "id": row["id"],
                                "title": row["title"],
                                "code": row["code"],
                                "date": row["date"],
                                "description": row["description"],
                            }
                        )
                else:
                    # 无keyword时，返回所有项
                    reviews.append(
                        {
                            "id": row["id"],
                            "title": row["title"],
                            "code": row["code"],
                            "date": row["date"],
                            "description": row["description"],
                        }
                    )

        # 6. 构建返回结果
        return {
            "success": True,
            "data": reviews,
            "count": len(reviews),
            "message": f"获取{type}类型评论成功（搜索关键字：{keyword or '无'}）",
        }
    except Exception as e:
        return {"success": False, "message": f"读取失败: {str(e)}"}, 500


def add_stock_review(_, request_body: Dict) -> Dict:
    """添加股票评论（按类型区分存储）"""
    if "type" not in request_body:
        return {"success": False, "message": "缺少type参数"}, 400

    type = request_body["type"]
    code = request_body.get("code", "").strip().upper()
    title = request_body.get("title", "").strip()
    date = request_body.get("date", "").strip()
    description = request_body.get("description", "").strip()

    try:
        csv_path = get_csv_path(type)
        init_csv_file(type)  # 确保文件存在
        rows: List[Dict] = []

        # 读取现有数据
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # 添加新数据
        new_item = {
            "id": str(uuid.uuid4()),  # 确保UUID是字符串类型
            "code": code,
            "title": title,
            "date": date,
            "description": description,
        }
        rows.append(new_item)

        # 写回所有数据
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {"success": True, "data": new_item, "message": f"添加{type}类型评论成功"}
    except Exception as e:
        return {"success": False, "message": f"添加失败: {str(e)}"}, 500


def get_single_stock_review(params: Dict) -> Dict:
    """获取单条股票评论（按类型和ID）"""
    if "type" not in params or "id" not in params:
        return {"success": False, "message": "缺少type或id参数"}, 400

    type = params["type"]
    target_id = (
        params["id"][0].strip()
        if isinstance(params["id"], list)
        else params["id"].strip()
    )

    try:
        csv_path = get_csv_path(type)
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] == target_id:
                    return {
                        "success": True,
                        "data": row,
                        "message": f"获取{type}类型评论成功",
                    }

        return {
            "success": False,
            "message": f"未找到ID为{target_id}的{type}类型评论",
        }, 404
    except Exception as e:
        return {"success": False, "message": f"查询失败: {str(e)}"}, 500


def delete_stock_review(_, request_body: Dict) -> Dict:
    """删除股票评论（按类型和ID）"""
    if "type" not in request_body or "id" not in request_body:
        return {"success": False, "message": "缺少type或id参数"}, 400

    type = request_body["type"]
    target_id = request_body["id"].strip()
    csv_path = get_csv_path(type)

    try:
        rows: List[Dict] = []
        found = False

        # 读取并过滤数据
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] != target_id:
                    rows.append(row)
                else:
                    found = True

        if not found:
            return {
                "success": False,
                "message": f"未找到ID为{target_id}的{type}类型评论",
            }, 404

        # 写回过滤后的数据
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {"success": True, "data": True, "message": f"删除{type}类型评论成功"}
    except Exception as e:
        return {"success": False, "message": f"删除失败: {str(e)}"}, 500
