import type { RouteObject } from 'react-router-dom';
import Home from '@/pages/Home';
import App from '@/pages/App';
import StockDetails from '../pages/StockDetails';
import PositionReview from '@/pages/PositionReview';
import PositionReviewDetails from '@/pages/PositionReviewDetails';
export const routes: RouteObject[] = [
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Home /> },
      {
        path: 'kline/:id',
        element: <StockDetails />,
      },
      {
        path: '/rs',
        element: <PositionReview />,
      },
      {
        path: '/rs/:id',
        element: <PositionReviewDetails />,
      },
    ],
  },
];
