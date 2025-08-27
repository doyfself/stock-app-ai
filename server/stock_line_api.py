import csv
import os
import json
from typing import List, Dict, Optional


# 画线数据存储目录
LINES_DIR = "lines"
# CSV表头（id不再单独列，lines数组内包含id）
LINE_HEADERS = ["code", "period", "lines", "width", "height"]


def init_line_dir():
    """初始化画线数据目录，确保目录存在"""
    if not os.path.exists(LINES_DIR):
        os.makedirs(LINES_DIR, exist_ok=True)


def get_line_file_path(code: str) -> str:
    """获取指定股票代码的画线文件路径（统一大写代码）"""
    init_line_dir()
    return os.path.join(LINES_DIR, f"{code.upper()}.csv")


def _find_row_by_code_period(
    file_path: str, code: str, period: str
) -> tuple[Optional[Dict], List[Dict]]:
    """
    工具函数：从CSV中查找code+period匹配的行
    返回：(匹配的行, 所有行列表)
    """
    all_rows = []
    target_row = None
    if os.path.exists(file_path):
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            all_rows = list(reader)
            # 查找code（大写）和period完全匹配的行
            for row in all_rows:
                if row["code"].upper() == code.upper() and row["period"] == period:
                    target_row = row
                    break
    return target_row, all_rows


def query_lines(_, request_body: Dict) -> Dict:
    """
    查询指定股票和周期的画线数据
    返回：{ code, period, lines, width, height } 完整对象（无数据则返回空对象）
    """
    code = request_body.get("code", "").strip()
    period = request_body.get("period", "").strip()

    # 参数校验
    if not code or not period:
        return {"success": False, "message": "code和period为必填参数"}, 400

    file_path = get_line_file_path(code)
    target_row, _ = _find_row_by_code_period(file_path, code, period)

    if not target_row:
        # 无匹配数据时返回空对象（符合前端"无数据"预期）
        return {
            "success": True,
            "data": {
                "code": code,
                "period": period,
                "lines": [],
                "width": 0,
                "height": 0,
            },
            "message": "未找到匹配的画线数据",
        }

    try:
        # 解析lines字段（JSON字符串转数组）
        lines = json.loads(target_row["lines"]) if target_row["lines"].strip() else []
        # 组装返回数据（确保类型正确）
        result = {
            "code": target_row["code"],
            "period": target_row["period"],
            "lines": lines,
            "width": int(target_row["width"]) if target_row["width"].strip() else 0,
            "height": int(target_row["height"]) if target_row["height"].strip() else 0,
        }
        return {"success": True, "data": result, "message": "画线数据查询成功"}

    except json.JSONDecodeError:
        # lines字段解析失败时返回空数组
        return {
            "success": True,
            "data": {
                "code": code,
                "period": period,
                "lines": [],
                "width": 0,
                "height": 0,
            },
            "message": "画线数据格式异常，已返回空数据",
        }
    except Exception as e:
        return {"success": False, "message": f"查询失败: {str(e)}"}, 500


def add_line(_, request_body: Dict) -> Dict:
    """
    新增画线数据：按code+period匹配行，在lines数组中追加新线条（含id）
    若无匹配行则创建新行
    """
    # 必传参数校验
    required_fields = ["code", "period", "lines", "width", "height"]
    for field in required_fields:
        if field not in request_body:
            return {"success": False, "message": f"{field}为必填参数"}, 400

    # 提取参数并格式化
    code = request_body["code"].strip().upper()
    period = request_body["period"].strip()
    new_lines = request_body["lines"]  # 前端传入的新线条数组（需包含id）
    width = request_body["width"]
    height = request_body["height"]

    # 校验lines格式（必须是数组，且每个元素需包含id）
    if not isinstance(new_lines, list):
        return {"success": False, "message": "lines必须是数组格式"}, 400
    for line in new_lines:
        if not isinstance(line, dict) or "id" not in line:
            return {"success": False, "message": "lines数组元素必须包含id字段"}, 400

    # 校验width和height（确保是数字）
    try:
        width = int(width) if not isinstance(width, int) else width
        height = int(height) if not isinstance(height, int) else height
    except (ValueError, TypeError):
        return {"success": False, "message": "width和height必须是有效数字"}, 400

    file_path = get_line_file_path(code)
    target_row, all_rows = _find_row_by_code_period(file_path, code, period)

    try:
        if target_row:
            # 已有匹配行：读取原有lines并追加新线条
            existing_lines = (
                json.loads(target_row["lines"]) if target_row["lines"].strip() else []
            )
            # 去重追加（避免重复id）
            new_line_ids = {line["id"] for line in new_lines}
            existing_lines = [
                line for line in existing_lines if line["id"] not in new_line_ids
            ]
            existing_lines.extend(new_lines)
            # 更新目标行数据
            target_row["lines"] = json.dumps(existing_lines, ensure_ascii=False)
            target_row["width"] = str(width)
            target_row["height"] = str(height)
            # 替换原数组中的目标行
            for i, row in enumerate(all_rows):
                if row["code"].upper() == code and row["period"] == period:
                    all_rows[i] = target_row
                    break
        else:
            # 无匹配行：创建新行
            new_row = {
                "code": code,
                "period": period,
                "lines": json.dumps(new_lines, ensure_ascii=False),
                "width": str(width),
                "height": str(height),
            }
            all_rows.append(new_row)

        # 写回文件
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=LINE_HEADERS)
            writer.writeheader()
            writer.writerows(all_rows)

        return {
            "success": True,
            "data": {"code": code, "period": period, "addedCount": len(new_lines)},
            "message": "画线数据添加成功",
        }

    except Exception as e:
        return {"success": False, "message": f"添加失败: {str(e)}"}, 500


def delete_line(_, request_body: Dict) -> Dict:
    """
    删除画线数据：按code+period找到行，删除lines数组中id匹配的元素
    """
    # 参数校验
    code = request_body.get("code", "").strip()
    period = request_body.get("period", "").strip()
    line_id = request_body.get("id", "")
    if not code or not period or not line_id:
        return {"success": False, "message": "code、period和id为必填参数"}, 400

    file_path = get_line_file_path(code)
    target_row, all_rows = _find_row_by_code_period(file_path, code, period)

    # 检查行是否存在
    if not target_row:
        return {
            "success": False,
            "message": f"未找到code={code}且period={period}的画线数据",
        }, 404

    try:
        # 解析lines数组
        lines = json.loads(target_row["lines"]) if target_row["lines"].strip() else []
        # 过滤掉id匹配的元素
        original_count = len(lines)
        lines = [line for line in lines if line.get("id") != line_id]

        if len(lines) == original_count:
            # 未找到对应id的线条
            return {"success": False, "message": f"未找到id={line_id}的画线数据"}, 404

        # 更新行数据
        target_row["lines"] = json.dumps(lines, ensure_ascii=False)
        # 替换原数组中的目标行
        for i, row in enumerate(all_rows):
            if row["code"].upper() == code and row["period"] == period:
                all_rows[i] = target_row
                break

        # 写回文件
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=LINE_HEADERS)
            writer.writeheader()
            writer.writerows(all_rows)

        return {
            "success": True,
            "data": {"remainingCount": len(lines)},
            "message": f"成功删除id={line_id}的画线数据",
        }

    except json.JSONDecodeError:
        return {"success": False, "message": "画线数据格式异常，无法删除"}, 400
    except Exception as e:
        return {"success": False, "message": f"删除失败: {str(e)}"}, 500
