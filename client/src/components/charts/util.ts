import klineConfig from './config';
import type {KlineDataType} from './types'
export function mapKlineToSvg(svgHeight:number, minPrice:number, maxPrice:number) {
    // 计算实际可用高度（减去上下边距）
    const availableHeight = svgHeight - klineConfig.padding * 2;
    
    // 计算价格范围
    const priceRange = maxPrice - minPrice;
    
    // 价格到Y坐标的映射函数
    // 注意：SVG的Y轴向下为正，所以需要反转
    const priceToY = (price:number) => {
        const ratio = (maxPrice - price) / priceRange;
        return klineConfig.padding + ratio * availableHeight;
    };
    return priceToY;
}

export function formatNumber(num: number) {
  // 检查是否为有效数字
  if (typeof num !== 'number' || isNaN(num)) {
    return num; // 非数字则返回原值
  }

  if (num >= 10) {
    // 大于等于10则取整
    return Math.round(num);
  } else if (num >= 1) {
    // 大于等于1且小于10则保留1位小数
    return Number(num.toFixed(1));
  } else {
    // 小于1则保留2位小数
    return Number(num.toFixed(2));
  }
}

export function calculateMA(data:KlineDataType[], period:number): number[] {
    // 验证输入
    if (!Array.isArray(data) || data.length === 0) {
        return []; // 如果数据为空，返回空数组
    }
    
    const result = [];
    
    // 遍历所有K线数据
    for (let i = 0; i < data.length; i++) {
        // 前period-1个数据点无法计算均线，用null表示
        if (i < period - 1) {
            result.push(-1);
            continue;
        }
        
        // 计算从i-period+1到i的收盘价平均值
        let sum = 0;
        for (let j = 0; j < period; j++) {
            // 确保数据点有收盘价属性
            if (data[i - j] && typeof data[i - j].close === 'number') {
                sum += data[i - j].close;
            } else {
                throw new Error(`第${i - j}个数据点缺少有效的收盘价`);
            }
        }
        // 计算平均值并保留适当的小数位数
        const average = sum / period;
        result.push(Number(average.toFixed(2))); // 保留两位小数
    }
    return result;
}