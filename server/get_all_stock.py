import akshare as ak
import pandas as pd
import os

def get_and_save_stock_data(csv_file="stock_codes_names.csv"):
    """
    获取所有A股股票的代码和名称，保存到CSV文件（仅包含这两个字段）
    若文件已存在则跳过获取过程
    """
    # 检查文件是否已存在
    if os.path.exists(csv_file):
        print(f"文件 {csv_file} 已存在，无需重复生成")
        return
    
    try:
        print("正在获取A股股票代码和名称...")
        
        # 获取A股股票数据
        stock_df = ak.stock_zh_a_spot()
        
        # 处理不同版本AKShare返回的列名差异
        if '代码' in stock_df.columns and '名称' in stock_df.columns:
            # 提取代码和名称列
            result_df = stock_df[['代码', '名称']]
        elif 'symbol' in stock_df.columns and 'name' in stock_df.columns:
            # 适配可能的英文列名
            result_df = stock_df[['symbol', 'name']].rename(
                columns={'symbol': '代码', 'name': '名称'}
            )
        else:
            # 如果列名不匹配，尝试查找包含"代码"和"名称"含义的列
            code_col = next((col for col in stock_df.columns if '代码' in col or 'symbol' in col.lower()), None)
            name_col = next((col for col in stock_df.columns if '名称' in col or 'name' in col.lower()), None)
            
            if not code_col or not name_col:
                raise ValueError("无法识别股票数据中的代码和名称列")
            
            result_df = stock_df[[code_col, name_col]].rename(
                columns={code_col: '代码', name_col: '名称'}
            )
        
        # 去重处理（避免可能的重复数据）
        result_df = result_df.drop_duplicates(subset=['代码'])
        
        # 保存到CSV
        result_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        print(f"成功提取 {len(result_df)} 条股票数据（仅含代码和名称）")
        print(f"数据已保存到 {csv_file}")
        
    except Exception as e:
        print(f"获取数据失败: {str(e)}")
        # 尝试使用备选接口
        try:
            print("尝试使用备选接口获取基础股票列表...")
            stock_basic_df = ak.stock_zh_a_basic()
            if 'code' in stock_basic_df.columns and 'name' in stock_basic_df.columns:
                result_df = stock_basic_df[['code', 'name']].rename(
                    columns={'code': '代码', 'name': '名称'}
                )
                result_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
                print(f"备选接口成功，保存 {len(result_df)} 条数据到 {csv_file}")
        except Exception as e2:
            print(f"备选接口也失败: {str(e2)}")