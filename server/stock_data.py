import akshare as ak
import pandas as pd

# 设置中文显示
pd.set_option('display.unicode.east_asian_width', True)

def get_stock_info():
    """获取股票基本信息示例"""
    # 获取A股所有股票列表
    stock_code_list = ak.stock_zh_a_spot()
    print("A股股票列表（前10条）：")
    print(stock_code_list.head(10))
    
    return stock_code_list

def get_stock_history(symbol="000001", start_date="20230101", end_date="20231231"):
    """获取股票历史行情数据"""
    # 获取日K线数据
    stock_zh_a_daily = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, end_date=end_date, adjust="qfq")
    print(f"\n{symbol}股票历史行情（前10条）：")
    print(stock_zh_a_daily.head(10))
    
    return stock_zh_a_daily

def get_stock_realtime():
    """获取实时行情数据"""
    # 获取沪深京A股实时行情
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    print("\nA股实时行情（前10条）：")
    print(stock_zh_a_spot_df[['代码', '名称', '最新价', '涨跌幅', '成交量']].head(10))
    
    return stock_zh_a_spot_df

def get_stock_index():
    """获取指数数据"""
    # 获取上证指数数据
    stock_index_df = ak.stock_zh_index_daily(symbol="sh000001")
    print("\n上证指数历史数据（前10条）：")
    print(stock_index_df.head(10))
    
    return stock_index_df

if __name__ == "__main__":
    # 确保AKShare是最新版本
    # !pip install akshare --upgrade
    
    # 获取股票基本信息
    stock_list = get_stock_info()
    
    # 获取特定股票历史数据（以平安银行为例，代码000001）
    history_data = get_stock_history("000001")
    
    # 获取实时行情
    realtime_data = get_stock_realtime()
    
    # 获取指数数据
    index_data = get_stock_index()
    
    # 可以将数据保存为CSV文件
    # history_data.to_csv("000001_history.csv", index=False)
    # realtime_data.to_csv("realtime_data.csv", index=False)
    print("\n数据获取完成！")
    