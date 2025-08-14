import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, Dict

def calculate_date_range(period: str) -> Tuple[str, str]:
    """
    计算不同周期往前追溯200个单位的时间范围
    
    参数:
        period: 时间周期，支持 'day'(日)、'week'(周)、'month'(月)、'30min'(30分钟)、'60min'(60分钟)
    
    返回:
        元组 (start_date, end_date)，格式为字符串（日期：%Y%m%d，时间：%Y%m%d%H%M）
    """
    # 结束时间默认为当前时间
    end = datetime.now()
    
    # 根据周期计算开始时间（往前追溯200个单位）
    if period == 'daily':
        # 日周期：200天前
        start = end - timedelta(days=200)
        date_format = "%Y%m%d"  # 日期格式
        
    elif period == 'weekly':
        # 周周期：200周前（每周按7天计算）
        start = end - timedelta(weeks=200)
        date_format = "%Y%m%d"
        
    elif period == 'monthly':
        # 月周期：200个月前（每月按30天近似计算，精确计算需考虑实际月份天数）
        start = end - timedelta(days=200 * 30)
        date_format = "%Y%m%d"
        
    else:
        num = int(period)
        # 30分钟周期：200个30分钟前
        start = end - timedelta(minutes=200 * num)
        date_format = "%Y%m%d%H%M"  # 包含时间的格式

    # 格式化开始时间和结束时间
    start_date = start.strftime(date_format)
    end_date = end.strftime(date_format)
    
    return start_date, end_date

def get_kline_data(params):
    try:
        stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='30', adjust="qfq")
        print(stock_zh_a_minute_df)
        # 1. 提取并验证参数
        code = params.get('code', [''])[0].strip()
        period = params.get('period', ['daily'])[0].strip().lower()
        if not code:
            return {'success': False, 'message': '缺少股票代码参数（code）'}
        # 3. 计算日期范围
        start_date, end_date = calculate_date_range(period)
        print(period.isdigit(),'232')
        request_api = ak.stock_zh_a_hist_min_em if period.isdigit() else ak.stock_zh_a_hist
        # 如果周期是数字，则使用另外一个接口

        # 4. 获取K线数据
        kline_df = request_api(
            symbol=code,
            period=period,
            # start_date=start_date,
            # end_date=end_date,
            adjust="qfq"
        )

        # 5. 检查返回数据是否为空
        if kline_df.empty:
            return {'success': False, 'message': f'未获取到股票 {code} 的K线数据（可能已退市或代码错误）'}

        # 6. 限制最多返回100条数据（取最近的100条）
        if len(kline_df) > 100:
            kline_df = kline_df.tail(100)

        # 7. 转换数据格式
        result = []
        for _, row in kline_df.iterrows():
            # 确保日期为字符串格式
            date_str = row["日期"].strftime("%Y-%m-%d") if hasattr(row["日期"], 'strftime') else str(row["日期"])
            
            # 处理数值类型，防止转换错误
            try:
                open_val = round(float(row["开盘"]), 2)
                high_val = round(float(row["最高"]), 2)
                low_val = round(float(row["最低"]), 2)
                close_val = round(float(row["收盘"]), 2)
                volume_val = int(row["成交量"]) if pd.notna(row["成交量"]) else 0
            except (ValueError, TypeError) as e:
                return {'success': False, 'message': f'数据格式转换错误：{str(e)}'}

            result.append({
                "date": date_str,
                "open": open_val,
                "high": high_val,
                "low": low_val,
                "close": close_val,
                "volume": volume_val
            })

        return {
            'success': True,
            'count': len(result),
            'data': result,
            'message': f'成功获取{len(result)}条数据'
        }

    # 8. 全局异常捕获
    except Exception as e:
        # 捕获所有未处理的异常，返回具体错误信息
        return {'success': False, 'message': f'获取K线数据失败：{str(e)}'}
    