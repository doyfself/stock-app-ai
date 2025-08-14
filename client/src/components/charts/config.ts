export default {
    padding: 20, // 上下间距
    right: 60, // 右侧留白
    candleWidth: 8, // K线实体宽度
    candleMargin: 2, // K线间距
    riseColor: '#f44336', // 涨颜色
    fallColor: '#4caf50', // 跌颜色
    averageLineConfig: [
        {
            name: 'MA5',
            period: 5,
            color: '#ff9800' // 5日均线颜色
        },
        {
            name: 'MA10',
            period: 10,
            color: '#2196f3' // 10日均线颜色
        },
        {
            name: 'MA20',
            period: 20,
            color: '#9c27b0' // 20日均线颜色
        },
        {
            name: 'MA30',
            period: 30,
            color: '#009688' // 30日均线颜色
        }
    ],
    periodSelectOptions: [{
        label: '日K',
        value: 'daily'
    }, {
        label: '周K',
        value: 'weekly'
    }, {
        label: '月K',
        value: 'monthly'
    }, {
        label: '60m',
        value: '60'
    }, {
        label: '30m',
        value: '30'
    }, {
        label: '5m',
        value: '5'
    }, {
        label: '1m',
        value: '1'
    }] // 可选均线周期
}