import { useParams } from 'react-router-dom';
import { getKlineDataApi, type KlineDataItem } from '@/apis/api';
import { useEffect, useState } from 'react';
import StockKlineChartMain from '@/components/charts/StockKlineChartMain';

export default function StockDetails() {
  // 获取路由参数id
  const { id } = useParams<{ id: string }>();
  return (
    <div>
      <StockKlineChartMain code={id as string} width={1200} height={400} />
    </div>
  );
}
