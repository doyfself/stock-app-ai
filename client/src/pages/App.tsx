import SearchStock from '@/components/common/SearchStock';
import { Outlet } from 'react-router-dom';

export default function Home() {
  return (
    <div>
      <header>
        <SearchStock />
      </header>
      <Outlet />
    </div>
  );
}
