import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getSinglePositionReviewApi } from '@/apis/api';
export default function PositionReviewDetails() {
  // 获取路由参数id
  const { id } = useParams<{ id: string }>();
  useEffect(() => {
    if (id) {
      getSinglePositionReviewApi(id).then((res) => {
        if (res.success) {
          console.log(res.data);
        }
      });
    }
  }, [id]);
  return <div></div>;
}
