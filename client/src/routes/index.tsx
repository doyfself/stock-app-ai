import type { RouteObject } from 'react-router-dom';
import Home from '@/pages/Home';
import App from '@/pages/App';
import StockDetails from '../pages/StockDetails';
import StockReview from '@/pages/StockReview';
import StockReviewDetails from '@/pages/StockReviewDetails';
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
        path: '/sr/:type',
        element: <StockReview />,
      },
      {
        path: '/sr/:type/:id',
        element: <StockReviewDetails />,
      },
    ],
  },
];
