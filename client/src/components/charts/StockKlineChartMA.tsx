import { calculateMA } from './util';
import type { StockKlineChartChildProps } from './types';
import klineConfig from './config';
export default function App({
  data,
  coordinateX,
  mapToSvg,
}: Pick<StockKlineChartChildProps, 'data' | 'coordinateX' | 'mapToSvg'>) {
  return (
    <g>
      {klineConfig.averageLineConfig.map((item) => {
        const maList = calculateMA(data, item.period);
        let points = '';
        maList.forEach((item, index) => {
          if (item != -1) {
            points += `${coordinateX[index]} ${mapToSvg(item)},`;
          }
        });
        return (
          <polyline
            points={points.slice(0, -1)} // 去掉最后一个逗号
            fill="none"
            stroke={item.color}
            stroke-width="1"
          />
        );
      })}
    </g>
  );
}
