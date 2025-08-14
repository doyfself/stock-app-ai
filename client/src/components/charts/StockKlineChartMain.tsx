import type { StockKlineChartMainProps } from './types';
import StockKlineChartBg from './StockKlineChartBg';
import StockKlineChartCandle from './StockKlineChartCandle';
import StockKlineChartMa from './StockKlineChartMA';
import { mapKlineToSvg } from './util';
import klineConfig from './config';
import { Radio } from 'antd';
import { useEffect, useState, useMemo } from 'react';
import { getKlineDataApi, type KlineDataItem } from '@/apis/api';
export default function App({ code, width, height }: StockKlineChartMainProps) {
  const [data, setData] = useState<KlineDataItem[]>([]);
  const [maxPrice, setMaxPrice] = useState<number>(0);
  const [minPrice, setMinPrice] = useState<number>(0);
  const [coordinateX, setCoordinateX] = useState<number[]>([]);
  const [period, setPeriod] = useState<string>('daily');
  useEffect(() => {
    if (code) {
      // 调用API获取K线数据
      getKlineDataApi(code, period).then((response) => {
        if (response && response.data) {
          const newData = response.data;
          setData(newData);
          const maxPrice = Math.max(...newData.map((item) => item.high));
          const minPrice = Math.min(...newData.map((item) => item.low));
          const coordinateX = newData.map((_, index) => {
            return (
              index * (klineConfig.candleMargin + klineConfig.candleWidth) +
              klineConfig.candleWidth / 2
            );
          });

          setMaxPrice(maxPrice);
          setMinPrice(minPrice);
          setCoordinateX(coordinateX);
        }
      });
    }
  }, [code, period]);
  // 3. 缓存mapToSvg计算结果，依赖变化时再更新
  const mapToSvg = useMemo(
    () => mapKlineToSvg(height, minPrice, maxPrice),
    [height, minPrice, maxPrice],
  );

  return (
    <>
      <StockKlineChartPeriodSwtich period={period} setPeriod={setPeriod} />
      <svg width={width} height={height}>
        <StockKlineChartBg
          width={width}
          height={height}
          maxPrice={maxPrice}
          minPrice={minPrice}
        />
        <StockKlineChartCandle
          data={data}
          coordinateX={coordinateX}
          mapToSvg={mapToSvg}
        />
        <StockKlineChartMa
          data={data}
          coordinateX={coordinateX}
          mapToSvg={mapToSvg}
        />
      </svg>
    </>
  );
}
interface StockKlineChartPeriodSwtichProps {
  period: string;
  setPeriod: (period: string) => void;
}
const StockKlineChartPeriodSwtich = ({
  period,
  setPeriod,
}: StockKlineChartPeriodSwtichProps) => {
  return (
    <Radio.Group
      defaultValue={period}
      size="small"
      onChange={(e) => setPeriod(e.target.value)}
    >
      {klineConfig.periodSelectOptions.map((item) => (
        <Radio.Button value={item.value} key={item.value}>
          {item.label}
        </Radio.Button>
      ))}
    </Radio.Group>
  );
};
