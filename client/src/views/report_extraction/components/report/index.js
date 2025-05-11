export default {
  data() {
    return {
      investment_outside_data: [
        {
          id: "1",
          option: {
            title: {
              text: "投资行业",
              subtext: "占比",
              left: "center",
            },
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b}: {c} ({d}%)",
            },
            legend: {
              orient: "vertical",
              left: "right",
              top: "middle",
              data: [
                "制造业(27) - 37.50%",
                "批发和零售业(15) - 20.83%",
                "科学研究和技术服务业(14) - 19.54%",
                "电力、热力、燃气及水生产和供应业(5) - 6.76%",
                "租赁和商务服务业(9) - 12.50%",
                "农、林、牧、渔业(2) - 2.70%",
                "房地产业(4) - 5.41%",
                "金融业(3) - 3.92%",
                "文化、体育和娱乐业(1) - 1.35%",
                "水利、环境和公共设施管理业(1) - 1.35%",
              ],
            },
            series: [
              {
                name: "投资行业",
                type: "pie",
                radius: "55%",
                center: ["30%", "50%"],
                data: [
                  { value: 27, name: "制造业(27) - 37.50%" },
                  { value: 15, name: "批发和零售业(15) - 20.83%" },
                  { value: 14, name: "科学研究和技术服务业(14) - 19.54%" },
                  {
                    value: 5,
                    name: "电力、热力、燃气及水生产和供应业(5) - 6.76%",
                  },
                  { value: 9, name: "租赁和商务服务业(9) - 12.50%" },
                  { value: 2, name: "农、林、牧、渔业(2) - 2.70%" },
                  { value: 4, name: "房地产业(4) - 5.41%" },
                  { value: 3, name: "金融业(3) - 3.92%" },
                  { value: 1, name: "文化、体育和娱乐业(1) - 1.35%" },
                  { value: 1, name: "水利、环境和公共设施管理业(1) - 1.35%" },
                ],
                emphasis: {
                  itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)",
                  },
                },
              },
            ],
          },
        },
        {
          id: "2",
          option: {
            title: {
              text: "登记状态",
              left: "center",
            },
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b}: {c} ({d}%)",
            },
            legend: {
              orient: "vertical",
              left: "right",
              top: "center",
              data: ["存续", "注销", "吊销", "迁出"],
            },
            series: [
              {
                name: "登记状态",
                type: "pie",
                radius: "55%",
                center: ["40%", "50%"],
                data: [
                  { value: 23, name: "存续" },
                  { value: 21, name: "注销" },
                  { value: 2, name: "吊销" },
                  { value: 1, name: "迁出" },
                ],
                emphasis: {
                  itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)",
                  },
                },
              },
            ],
          },
        },
        {
          id: "3",
          option: {
            title: {
              text: "投资地域",
              subtext: "省份投资企业数量",
              left: "center",
            },
            tooltip: {
              trigger: "item",
            },
            visualMap: {
              show: true,
              min: 0,
              max: 20,
              left: "left",
              top: "bottom",
              text: ["高", "低"],
              inRange: {
                color: ["#e0ffff", "#006edd"],
              },
              calculable: true,
            },
            legend: [
              {
                orient: "vertical",
                top: "middle",
                left: "right",
                data: ["江苏", "浙江", "上海", "北京", "海南"],
              },
            ],
            series: [
              {
                name: "投资地域",
                type: "map",
                map: "china",
                roam: false,
                label: {
                  show: true,
                },
                data: [
                  { name: "北京", value: 2 },
                  { name: "天津", value: 1 },
                  { name: "上海", value: 3 },
                  { name: "重庆", value: 0 },
                  { name: "河北", value: 0 },
                  { name: "河南", value: 0 },
                  { name: "云南", value: 0 },
                  { name: "辽宁", value: 0 },
                  { name: "黑龙江", value: 0 },
                  { name: "湖南", value: 0 },
                  { name: "安徽", value: 0 },
                  { name: "山东", value: 0 },
                  { name: "新疆", value: 0 },
                  { name: "江苏", value: 65 },
                  { name: "浙江", value: 4 },
                  { name: "江西", value: 0 },
                  { name: "湖北", value: 0 },
                  { name: "广西", value: 0 },
                  { name: "甘肃", value: 0 },
                  { name: "山西", value: 0 },
                  { name: "内蒙古", value: 0 },
                  { name: "陕西", value: 0 },
                  { name: "吉林", value: 0 },
                  { name: "福建", value: 0 },
                  { name: "贵州", value: 0 },
                  { name: "广东", value: 0 },
                  { name: "青海", value: 0 },
                  { name: "西藏", value: 0 },
                  { name: "四川", value: 0 },
                  { name: "宁夏", value: 0 },
                  { name: "海南", value: 2 },
                  { name: "台湾", value: 0 },
                  { name: "香港", value: 0 },
                  { name: "澳门", value: 0 },
                ],
              },
            ],
          },
        },
        {
          id: "4",
          option: {
            title: {
              text: "投资趋势",
            },
            tooltip: {
              trigger: "axis",
              axisPointer: {
                type: "shadow",
              },
            },
            legend: {
              data: ["投资数量"],
            },
            dataZoom: [
              {
                type: "slider",
                start: 0,
                end: 10,
                handleSize: "50%",
                handleStyle: {
                  color: "#000000",
                  shadowBlur: 3,
                  shadowColor: "rgba(0, 0, 0, 0.6)",
                  shadowOffsetX: 2,
                  shadowOffsetY: 2,
                },
              },
            ],
            xAxis: [
              {
                type: "category",
                data: [
                  "1994",
                  "1995",
                  "1996",
                  "1997",
                  "1998",
                  "1999",
                  "2000",
                  "2001",
                  "2002",
                  "2003",
                  "2004",
                  "2005",
                  "2006",
                  "2007",
                  "2008",
                  "2009",
                  "2010",
                  "2011",
                  "2012",
                  "2013",
                  "2014",
                  "2015",
                  "2016",
                  "2017",
                  "2018",
                  "2019",
                  "2020",
                  "2021",
                  "2022",
                  "2023",
                ],
                axisPointer: {
                  type: "shadow",
                },
              },
            ],
            yAxis: [
              {
                type: "value",
              },
            ],
            series: [
              {
                name: "投资数量",
                type: "bar",
                barWidth: "20%", // 调整柱子宽度
                data: [
                  1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1,
                ],
              },
            ],
          },
        },
      ],
      judicial_case_table:{
        id:"56",
        option:{
          "title": {
            "text": "案件趋势",
            "left": "3%",
            "textStyle": {
              fontSize:14
            }
          },
          "tooltip": {
            "trigger": "axis",
            "axisPointer": {
              "type": "shadow"
            }
          },
          "legend": {
            "data": ["原告", "被告", "其他"],
            "bottom": 10,
            "align": "center",
            "textStyle": {
              "color": "#000"
            }
          },
          "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "7%",
            "containLabel": true
          },
          "xAxis": {
            "type": "category",
            "data": ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2013"]
          },
          "yAxis": {
            "type": "value"
          },
          "series": [
            {
              "name": "原告",
              "type": "bar",
              "stack": "total",
              "label": {
                "show": true,
                "position": "insideRight"
              },
              "data": [10, 5, 7, 3, 6, 4, 2, 3, 1, 0, 0],
              "itemStyle": {
                "color": "#2f4554"
              },
              "barWidth": "20%"
            },
            {
              "name": "被告",
              "type": "bar",
              "stack": "total",
              "label": {
                "show": true,
                "position": "insideRight"
              },
              "data": [15, 10, 9, 6, 8, 5, 3, 4, 2, 1, 1],
              "itemStyle": {
                "color": "#d53a35"
              },
              "barWidth": "20%"
            },
            {
              "name": "其他",
              "type": "bar",
              "stack": "total",
              "label": {
                "show": true,
                "position": "insideRight"
              },
              "data": [5, 8, 6, 4, 2, 3, 1, 2, 1, 0, 1],
              "itemStyle": {
                "color": "#546570"
              },
              "barWidth": "20%"
            }
          ],
          "dataZoom": [
            {
              "type": "slider",
              "start": 0,
              "end": 50,
              "handleSize": "0%",
              "handleStyle": {
                "color": "#000",
                "shadowBlur": 3,
                "shadowColor": "rgba(0, 0, 0, 0.6)",
                "shadowOffsetX": 2,
                "shadowOffsetY": 2
              }
            }
          ]
        }
      },
      patent_trend_table:{
        id:"6",
        option:{
          'title': {
            'text': '专利申请年份趋势',
            'left': 'upper left',
            'fontSize': 14
          },
          'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
              'type': 'shadow'
            }
          },
          'legend': {
            'data': ['发明专利', '外观专利', '实用新型'],
            'bottom': '0%',
            'textStyle': {
              'color': '#333'
            }
          },
          'xAxis': {
            'type': 'category',
            'data': ['2001', '2003', '2004', '2005', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
            'axisLabel': {
              'interval': 1
            },
            'axisTick': {
              'show': false
            },
            'axisLine': {
              'show': false
            }
          },
          'yAxis': {
            'type': 'value',
            'axisLine': {
              'show': false
            },
            'axisLabel': {
              'show': false
            },
            'splitLine': {
              'show': false
            }
          },
          'series': [
            {
              'name': '发明专利',
              'type': 'bar',
              'stack': 'total',
              'itemStyle': {
                'color': '#2f4554'
              },
              'barWidth': '20%',
              'data': [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 2, 23, 31]
            },
            {
              'name': '外观专利',
              'type': 'bar',
              'stack': 'total',
              'itemStyle': {
                'color': '#d53a35'
              },
              'barWidth': '20%',
              'data': [0, 3, 9, 1, 2, 3, 3, 3, 1, 2, 1, 1, 2, 2, 6, 8]
            },
            {
              'name': '实用新型',
              'type': 'bar',
              'stack': 'total',
              'itemStyle': {
                'color': '#546570'
              },
              'barWidth': '20%',
              'data': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 3, 3, 0, 0]
            }
          ],
          'dataZoom': [
            {
              'type': 'slider',
              'start': 0,
              'end': 50,
              'handleSize': '80%',
              'handleStyle': {
                'color': '#000',
                'shadowBlur': 3,
                'shadowColor': 'rgba(0, 0, 0, 0.6)',
                'shadowOffsetX': 2,
                'shadowOffsetY': 2
              }
            }
          ]
        }
      },
      patent_activate_table:{
        id:"7",
        option:{
          "title": {
            "text": "发明人专利申请活跃度"
          },
          "tooltip": {},
          "legend": {
            "data": ["尹秀丽", "于燕", "曹文明", "朱新宇", "臧影影"],
            "top":"bottom"
          },
          "radar": {
            "indicator": [
              {"name": "2024", "max": 10},
              {"name": "2023", "max": 10},
              {"name": "2022", "max": 10},
              {"name": "2021", "max": 10},
              {"name": "2020", "max": 10}
            ],
            "center": ["50%", "50%"],
            "radius": 100
          },
          "series": [{
            "name": "发明人专利申请",
            "type": "radar",
            "data": [
              {
                "value": [5, 3, 2, 1, 0],
                "name": "尹秀丽"
              },
              {
                "value": [3, 4, 1, 2, 1],
                "name": "于燕"
              },
              {
                "value": [2, 1, 1, 1, 0],
                "name": "曹文明"
              },
              {
                "value": [1, 2, 1, 0, 1],
                "name": "朱新宇"
              },
              {
                "value": [2, 1, 2, 1, 0],
                "name": "臧影影"
              }
            ]
          }]
        }
      }
    };
  },
};
