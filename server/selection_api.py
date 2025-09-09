import csv
import os

# 自选
# CSV文件路径
CSV_FILE = "selection.csv"
# CSV表头
CSV_HEADERS = ["code", "name", "color", "remark", "sort"]


def init_csv_file():
    """初始化CSV文件，如果不存在则创建并写入表头"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()


def get_selection(params=None):
    """获取自选列表（GET请求）"""
    init_csv_file()
    selections = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                selections.append(
                    {
                        "code": row["code"],
                        "name": row["name"],
                        "color": row["color"],
                        "remark": row["remark"],
                        "sort": row["sort"],
                    }
                )
        return {
            "success": True,
            "data": selections,
            "count": len(selections),
            "message": "自选列表获取成功",
        }
    except Exception as e:
        print(e)
        return {"success": False, "message": f"读取自选列表失败: {str(e)}"}, 500


def get_selection_remark(params=None):
    """根据code获取自选备注（GET请求）"""
    # 参数校验
    if not params or "code" not in params:
        return {"success": False, "message": "缺少code参数"}, 400

    # 处理code参数（兼容列表/字符串类型）
    code_param = params["code"]
    target_code = (
        code_param[0].strip().upper()
        if isinstance(code_param, list)
        else str(code_param).strip().upper()
    )

    if not target_code:
        return {"success": False, "message": "code参数不能为空"}, 400

    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 匹配code（不区分大小写）
                if row["code"].strip().upper() == target_code:
                    return {
                        "success": True,
                        "data": {
                            "code": row["code"],
                            "name": row["name"],
                            "color": row["color"],
                            "remark": row["remark"],
                            "sort": row["sort"],
                        },
                        "message": f"获取{target_code}备注成功",
                    }

        # 未找到对应code的记录
        return {
            "success": False,
            "message": f"未找到code为{target_code}的自选记录",
        }, 404

    except Exception as e:
        print(e)
        return {"success": False, "message": f"获取备注失败: {str(e)}"}, 500


def is_selection_exists(params):
    code = params.get("code", [""])[0].strip().upper()
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["code"][-6:] == code[-6:]:
                return {"success": True, "data": True}
    return {"success": True, "data": False}


def add_selection(_, request_body):
    code = request_body.get("code", "").strip().upper()
    # 只处理有效代码
    if not code:
        return {"success": False, "data": False, "message": "股票代码不能为空"}, 400

    # 提取需要更新的字段（值不为空才处理）
    update_fields = {}
    if request_body.get("name", "").strip():
        update_fields["name"] = request_body["name"].strip()
    if request_body.get("color", "").strip():
        update_fields["color"] = request_body["color"].strip()
    if request_body.get("remark", "").strip():
        update_fields["remark"] = request_body["remark"].strip()

    try:
        # 读取所有行并保留原始顺序
        rows = []
        item_index = -1  # 记录目标行的位置
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                # 匹配代码（取后6位）
                if row["code"][-6:] == code[-6:]:
                    item_index = idx
                    # 只更新传入的非空字段，其他字段保持不变
                    updated_row = {**row, **update_fields}
                    rows.append(updated_row)
                else:
                    rows.append(row)

        # 如果不存在则新增
        if item_index == -1:
            # 新行基础数据，缺失字段用空值填充
            new_row = {"code": code, "name": "", "color": "", "remark": "", "sort": ""}
            update_fields["sort"] = len(rows) + 1
            # 应用更新字段
            new_row.update(update_fields)
            rows.append(new_row)

        # 写回所有数据
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {"success": True, "data": True, "message": "自选项目添加/更新成功"}

    except Exception as e:
        return {"success": False, "data": False, "message": f"操作失败: {str(e)}"}, 500


def update_selection_sort(_, request_body):
    # 前端传递的完整代码顺序列表（按新排序排列）
    # 格式示例：["600000", "600036", "000001"...]
    new_order_codes = request_body.get("newOrderCodes", [])

    # 验证参数
    if not isinstance(new_order_codes, list) or len(new_order_codes) == 0:
        return {"success": False, "message": "请提供有效的新排序代码列表"}, 400

    try:
        # 1. 读取现有所有数据
        existing_rows = []
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_rows = list(reader)  # 转为列表便于处理

        # 2. 按新顺序重新组织数据
        # 2.1 先收集所有匹配新顺序的行
        ordered_rows = []
        code_set = {code[-6:].upper() for code in new_order_codes}  # 取后6位并去重

        for code in new_order_codes:
            code_suffix = code[-6:].upper()
            # 查找匹配的行
            for row in existing_rows:
                if row["code"][-6:].upper() == code_suffix:
                    ordered_rows.append(row)
                    existing_rows.remove(row)  # 移除已匹配的行，避免重复
                    break

        # 2.2 剩余未在新顺序中出现的行追加到末尾（可选逻辑）
        ordered_rows.extend(existing_rows)

        # 3. 重新分配sort值（1,2,3...与行数一致）
        for idx, row in enumerate(ordered_rows):
            row["sort"] = str(idx + 1)  # 从1开始编号

        # 4. 写回CSV
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(ordered_rows)

        return {
            "success": True,
            "data": {
                "total": len(ordered_rows),
                "newSort": [row["sort"] for row in ordered_rows],
            },
            "message": "排序更新成功",
        }

    except Exception as e:
        return {"success": False, "message": f"排序更新失败: {str(e)}"}, 500


def delete_selection(_, request_body):
    """删除自选项目（POST请求）"""
    code = request_body.get("code", "").strip().upper()
    try:
        rows = []
        found = False

        # 读取所有行并查找要删除的项目
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["code"][-6:] != code[-6:]:
                    rows.append(row)
                else:
                    found = True

        if not found:
            return {"success": False, "message": f"未找到代码为 {code} 的自选项目"}, 404

        # 写回所有保留的行
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {
            "success": True,
            "data": True,
            "message": f"成功删除代码为 {code} 的自选项目",
        }
    except Exception as e:
        return {
            "success": False,
            "data": False,
            "message": f"删除自选项目失败: {str(e)}",
        }, 500
