import {
  getSelectionApi,
  getSelectionDetails,
  type SelectionItem,
  type SelectionDetailsItem,
} from '@/apis/api';
import { useSelectionStore } from '@/stores/userStore';
import { useEffect, useState } from 'react';
import { addStockCodePrefix, isInStockTradingTime } from '@/utils/common';
import './index.css';
import { useNavigate } from 'react-router-dom';
export default function App({ code }: { code: string }) {
  // 订阅刷新标识，当它变化时会触发组件更新
  const refreshFlag = useSelectionStore((state) => state.refreshFlag);
  const navigate = useNavigate();
  const [baseData, setBaseData] = useState<SelectionItem[]>([]);
  const [symbols, setSymbols] = useState<string>('');
  const [dynamicData, setDynamicData] = useState<SelectionDetailsItem[]>([]);
  const initData = () => {
    // 获取自选列表
    getSelectionApi().then((response) => {
      if (response && response.data) {
        setBaseData(response.data);
        setSymbols(response.data.map((item) => item.code).join(','));
      }
    });
  };
  useEffect(initData, []);
  useEffect(() => {
    if (refreshFlag > 0) initData();
  }, [refreshFlag]);
  useEffect(() => {
    // 存储定时器ID，用于清理
    let intervalId: NodeJS.Timeout;

    // 定义请求数据的函数
    const fetchData = async () => {
      if (symbols) {
        try {
          const response = await getSelectionDetails(symbols);
          if (response && response.data) {
            setDynamicData(response.data);
          }
        } catch (error) {
          console.error('获取股票详情失败:', error);
          // 可根据需求添加错误处理，如重试机制
        }
      }
    };

    // 立即执行一次请求
    fetchData();

    // 设置轮询：每隔5秒请求一次（时间可根据需求调整）
    if (symbols && isInStockTradingTime()) {
      intervalId = setInterval(fetchData, 1000);
    }

    // 清理函数：组件卸载或code变化时清除定时器
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [symbols]);
  const scanDetails = (code: string) => {
    navigate('/kline/' + code);
  };
  return (
    <div className="selection-list">
      <div className="selection-list-header">
        <span>名称</span>
        <span>涨幅/现价</span>
      </div>
      <ul>
        {dynamicData.map((item, index) => {
          return (
            <li
              className={code.includes(item.code) ? 'active' : ''}
              onClick={() => scanDetails(baseData[index].code)}
              key={item.code}
            >
              <div>
                <div>{item.name}</div>
                <div>{item.code}</div>
              </div>
              <div
                style={{
                  color: item.percent >= 0 ? 'red' : 'green',
                }}
              >
                <div>{item.percent}%</div>
                <div>{item.current}</div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
