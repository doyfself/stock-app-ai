import csv
import uuid
import os

# 自选
# CSV文件路径
CSV_FILE = "position_review.csv"
# CSV表头
CSV_HEADERS = ["id", "title", "code", "date", "description"]


def init_csv_file():
    """初始化CSV文件，如果不存在则创建并写入表头"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()


def get_position_review(params=None):
    init_csv_file()
    selections = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                selections.append(
                    {
                        "id": row["id"],
                        "title": row["title"],
                        "code": row["code"],
                        "date": row["date"],
                        "description": row["description"],
                    }
                )
        return {
            "success": True,
            "data": selections,
            "count": len(selections),
            "message": "获取成功",
        }
    except Exception as e:
        print(e)
        return {"success": False, "message": f"读取失败: {str(e)}"}, 500


def add_position_review(_, request_body):
    code = request_body.get("code", "").strip().upper()
    title = request_body.get("title", "").strip()
    date = request_body.get("date", "").strip()
    description = request_body.get("description", "").strip()

    try:
        rows = []

        # 读取所有行
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)

        rows.append(
            {
                "id": uuid.uuid4(),
                "code": code,
                "title": title,
                "date": date,
                "description": description,
            }
        )

        # 写回所有数据
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {"success": True, "data": True, "message": "添加成功"}
    except Exception as e:
        return {"success": False, "data": False, "message": f"添加失败: {str(e)}"}, 500


def get_single_position_review(params):
    id = params.get("id", [""])[0].strip().lower()
    try:

        # 读取所有行并查找要删除的项目
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] != id:
                    return {"success": True, "data": row, "message": "添加成功"}

        return {
            "success": False,
            "data": False,
            "message": f"删除自选项目失败: {str(e)}",
        }, 500
    except Exception as e:
        return {
            "success": False,
            "data": False,
            "message": f"删除自选项目失败: {str(e)}",
        }, 500


def delete_position_review(_, request_body):
    """删除项目（POST请求）"""
    id = request_body.get("id", "").strip().upper()
    try:
        rows = []
        found = False

        # 读取所有行并查找要删除的项目
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] != id:
                    rows.append(row)
                else:
                    found = True

        if not found:
            return {"success": False, "message": f"未找到项目"}, 404

        # 写回所有保留的行
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        return {"success": True, "data": True, "message": f"成功删除"}
    except Exception as e:
        return {
            "success": False,
            "data": False,
            "message": f"删除自选项目失败: {str(e)}",
        }, 500
