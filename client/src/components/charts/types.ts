export interface KlineDataType {
    date: string; // 日期格式：YYYY-MM-DD
    open: number; // 开盘价
    high: number; // 最高价
    low: number; // 最低价
    close: number; // 收盘价
    volume: number; // 成交量
}

export interface StockKlineChartMainProps {
  code: string;
  width: number;
  height: number;
}
export interface StockKlineChartChildProps extends Pick<StockKlineChartMainProps, 'width' | 'height'> {
    data: KlineDataType[];
    maxPrice: number;
    minPrice: number;
    coordinateX: number[]; // X轴坐标数组
    mapToSvg: (price:number) => number; // 将价格映射到SVG坐标
}