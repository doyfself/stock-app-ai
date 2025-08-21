import './index.css';
import SearchStock from './SearchStock';
import { Link } from 'react-router-dom';
export default function App() {
  return (
    <div className="header-nav">
      <div className="flex-1"></div>
      <SearchStock />
      <Link to="/rs">持仓三省</Link>
      <Link to="">欲购三省</Link>
      <Link to="">自选</Link>
    </div>
  );
}
