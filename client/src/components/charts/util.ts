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

/**
 * 将成交量数值转换为"xx万""xx亿"格式，保留两位小数
 * @param volume 原始成交量数值（如1234567、8901234567等）
 * @returns 格式化后的字符串（如"123.46万"、"89.01亿"）
 */
export const formatVolume = (volume: number): string => {
  // 处理非数字或负数情况（成交量通常非负）
  if (isNaN(volume) || volume < 0) {
    return "0.00万";
  }

  // 定义单位转换阈值（1亿 = 10000万 = 10^8，1万 = 10^4）
  const 亿 = 100000000;
  const 万 = 10000;

  // 根据数值大小选择单位并转换
  if (volume >= 亿) {
    // 大于等于1亿时，转换为“亿”单位
    const value = volume / 亿;
    return `${value.toFixed(2)}亿`;
  } else if (volume >= 万) {
    // 大于等于1万且小于1亿时，转换为“万”单位
    const value = volume / 万;
    return `${value.toFixed(2)}万`;
  } else {
    // 小于1万时，直接保留两位小数（不添加单位）
    return volume.toFixed(2);
  }
};

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