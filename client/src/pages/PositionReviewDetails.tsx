import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { addStockCodePrefix } from '@/utils/common';
import {
  getSinglePositionReviewApi,
  type PositionReviewItem,
} from '@/apis/api';
import StockKlineChartMain from '@/components/charts/StockKlineChartMain';
export default function PositionReviewDetails() {
  // 获取路由参数id
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<PositionReviewItem | null>(null);
  useEffect(() => {
    if (id) {
      getSinglePositionReviewApi(id).then((res) => {
        if (res.success) {
          setData(res.data as PositionReviewItem);
        }
      });
    }
  }, [id]);
  if (data) {
    return (
      <div className="pv-details-container">
        <h2>
          {data.title}({data.code})
        </h2>
        <StockKlineChartMain
          code={addStockCodePrefix(data.code)}
          width={800}
          height={300}
          timestamp={data.date}
          limit={50}
        />
        <p dangerouslySetInnerHTML={{ __html: data.description }}></p>
      </div>
    );
  }
}
