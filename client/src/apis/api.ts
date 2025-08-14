import request from '../utils/request';
type QueryStockByWordResponse = {
    代码:string;
    名称:string;
}[];
export const queryStockByWordApi = (w:string) => request.get<QueryStockByWordResponse>('/search?w=' + w);
// 定义 K 线数据类型接口
export interface KlineDataItem {
  date: string; // 日期格式：YYYY-MM-DD
  open: number; // 开盘价
  high: number; // 最高价
  low: number; // 最低价
  close: number; // 收盘价
  volume: number; // 成交量
}
export const getKlineDataApi = (code: string, period: string) => request.get<KlineDataItem[]>(`/kline?code=${code}&period=${period}`)