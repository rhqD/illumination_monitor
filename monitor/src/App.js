import { useRef, useEffect } from "react";
import "./App.css";
const echarts = require("echarts");

const baseOption = {
  title: {
    text: '动态数据 + 时间坐标轴'
  },
  tooltip: {
    trigger: 'axis',
    formatter: function (params) {
      params = params[0];
      var date = new Date(params.name);
      return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + '  ' + date.getHours() + ' : ' + date.getMinutes() + ' ' + ' : ' + params.value[1];
    },
    axisPointer: {
      animation: false
    }
  },
  xAxis: {
    type: 'time',
    splitLine: {
      show: false
    }
  },
  yAxis: {
    type: 'value',
    boundaryGap: [0, '100%'],
    splitLine: {
      show: false
    }
  },
  series: [{
    name: '模拟数据',
    type: 'line',
    showSymbol: false,
    hoverAnimation: false,
  }]
};

function App() {
  const containerRef = useRef();
  const myCharts = useRef();
  useEffect(() => {
    myCharts.current = echarts.init(containerRef.current);
    fetch('/data').then(resp => resp.json()).then(({ data }) => {
      baseOption.series[0].data = data.map(it => {
        const time = new Date(it.time);
        return {
          name: time.toString(),
          value: [
              time,
              0 - it.value
          ]
        };
      });
      myCharts.current.setOption(baseOption);
    });
  });
  return (
    <div className="App" ref={containerRef}>

    </div>
  );
}

export default App;
