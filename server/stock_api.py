import pandas as pd
def fuzzy_match_stocks(stock_df, keyword, top_n=10):
    if not keyword or stock_df.empty:
        return pd.DataFrame()
    
    # 确保代码为字符串类型
    stock_df['代码'] = stock_df['代码'].astype(str)
    
    # 1. 计算匹配分数：位置越靠前，分数越高
    def calculate_score(row):
        code = row['代码']
        name = row['名称']
        score = 0
        
        # 代码匹配（权重高于名称）
        if keyword in code:
            # 位置越靠前分数越高（例如长度为10的字符串，位置0得10分，位置9得1分）
            code_pos = code.index(keyword)
            code_length = len(code)
            score += (code_length - code_pos) * 2  # 代码匹配权重翻倍
        
        # 名称匹配
        if keyword in name:
            name_pos = name.index(keyword)
            name_length = len(name)
            score += (name_length - name_pos)
        
        return score
    
    # 2. 计算所有行的分数
    stock_df['match_score'] = stock_df.apply(calculate_score, axis=1)
    
    # 3. 筛选出有匹配的结果，并按分数降序排序
    matched = stock_df[stock_df['match_score'] > 0]
    sorted_results = matched.sort_values(by='match_score', ascending=False)
    
    # 4. 移除临时列，返回前N项
    return sorted_results.drop(columns=['match_score']).head(top_n)
def query_stock_by_word(params):
    """根据查询参数返回股票代码和名称"""
    
    keyword = params.get('w', [''])[0].strip()
    
    if not keyword:
        return {'success': False, 'message': '缺少查询关键词'}, 400
    
    try:
        # 读取股票数据
        stock_df = pd.read_csv("stock_codes_names.csv", encoding="utf-8-sig")
        
        # 进行模糊匹配
        results = fuzzy_match_stocks(stock_df, keyword, 10)
        print(results)
        
        # 格式化结果
        result_list = results.to_dict(orient='records')
        
        return {
            'success': True,
            'data': result_list,
            'count': len(result_list)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500


