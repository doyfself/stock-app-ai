import csv
import os
# 自选
# CSV文件路径
CSV_FILE = "selection.csv"
# CSV表头
CSV_HEADERS = ["code", "name", "color", "remark"]
def init_csv_file():
    """初始化CSV文件，如果不存在则创建并写入表头"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()

def get_selection(params=None):
    """获取自选列表（GET请求）"""
    init_csv_file()
    selections = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                selections.append({
                    "code": row["code"],
                    "name": row["name"],
                    "color": row["color"],
                    "remark": row["remark"]
                })
        return {
            'success': True,
            'data': selections,
            'count': len(selections),
            'message': '自选列表获取成功'
        }
    except Exception as e:
        print(e)
        return {'success': False, 'message': f'读取自选列表失败: {str(e)}'}, 500
    
def is_selection_exists(params):
    code = params.get('code', [''])[0].strip().upper()
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['code'][-6:] == code[-6:]:
                return {'success': True, 'data': True}
    return {'success': True, 'data': False}
    
def add_selection(_,request_body):
    code = request_body.get('code', '').strip().upper()
    name = request_body.get('name', '').strip()
    color = request_body.get('color', '').strip()
    remark = request_body.get('remark', '').strip()
    try:
        rows = []
        item_exists = False
        
        # 读取所有行
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 如果找到相同代码，替换为新数据
                if row['code'][-6:] == code[-6:]:
                    rows.append({
                        'code': code,
                        'name': name,
                        'color': color,
                        'remark': remark
                    })
                    item_exists = True
                else:
                    rows.append(row)
        
        # 如果不存在，则添加到末尾
        if not item_exists:
            rows.append({
                        'code': code,
                        'name': name,
                        'color': color,
                        'remark': remark
                    })
        
        # 写回所有数据
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)
        
        return {'success': True,'data': True, 'message': '自选项目添加/更新成功'}
    except Exception as e:
        return {'success': False,'data': False, 'message': f'添加自选项目失败: {str(e)}'}, 500

def delete_selection(_,request_body):
    """删除自选项目（POST请求）"""
    code = request_body.get('code', '').strip().upper()
    try:
        rows = []
        found = False
        
        # 读取所有行并查找要删除的项目
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['code'][-6:] != code[-6:]:
                    rows.append(row)
                else:
                    found = True
        
        if not found:
            return {'success': False, 'message': f'未找到代码为 {code} 的自选项目'}, 404
        
        # 写回所有保留的行
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)
        
        return {'success': True, 'data': True, 'message': f'成功删除代码为 {code} 的自选项目'}
    except Exception as e:
        return  {'success': False, 'data': False, 'message': f'删除自选项目失败: {str(e)}'}, 500