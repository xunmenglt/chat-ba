# 对外投资分析-投资行业
graph_outward_investment_investment_industry_template="""
# 角色
- 你是一个echart绘图专家

# 任务
- 基于‘参考内容’和‘要求’，帮我按要求生成echart相关代码。

# 模板
## echart模板
- 以下是echart对应的option模板：
【echart-option模板开始】
```json
{
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
}
```
【echart-option模板结束】

# 参考内容
【参考内容开始】
{context}
【参考内容结束】

# 要求

## 模板转换要求： 
- 按照给定的echart-option模板，填补或替换模板中的数据，生成echart对应的option代码
- echart-option模板中的title为表格名称，固定为‘投资行业’，无需更改
- legend对应‘参考内容’中的所属行业对应内容，你需要对其归类，归类的名称可以和所属行业字段对应的值相同，但最终类别数量不能超过6个，对其他次要的类别都归类为‘其他’类别。
    egend应该用圆点来做分割如下面这个格式：
    · 制造业(27)                  37.50%
    · 批发和零售业(15)        20.83%
- legend的中元素为表格中的所属行业，所以你应该对表格中的所属行业进行提取，并总结每个行业对应的被投资企业数量，其中上面的格式27和15就是两个行业对应的被投资企业数量，另外其中37%和20.83%是该行业对应的被投资企业在整个表格中所占据的数量比例。
- series中的data每个元素的value值总和要等于参考内容的被投资企业总数，务必保持相等
    - series中的data每个元素的value值等于该类别对应的被投资企业总数
- 转换后的option要与模板风格和样式务必保持一致
- 数据总数要和参考内容一致（如：行数），不能擅自删除和修改数据，不能擅自删除和修改数据。

## 输出要求
- 把上面的数据转化为echart option代码
- 请不要输出别的内容,输出格式如下：
```json
{'option':'echarts的option代码内容'}
```
- ‘【’和‘】’符号包裹的是提示文字，不必输出该符号以及其包裹的提示文字。
- 再次强调，务必严格按模板转换要求进行转换，样式保持一致，输出内容务必按输出模板输出，不要包含其他内容和解释内容！不要包含其他内容和解释内容！
"""

# 登记状态模板
graph_outward_investment_registration_status_template="""
# 角色
- 你是一个echart绘图专家

# 任务
- 基于‘参考内容’和‘要求’，帮我按要求生成echart相关代码。

# 模板
## echart模板
- 以下是echart对应的option模板：
【echart-option模板开始】
```json
{
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
}
```
【echart-option模板结束】

# 参考内容
【参考内容开始】
{context}
【参考内容结束】

# 要求

## 模板转换要求： 
- 按照给定的echart-option模板，填补或替换模板中的数据，生成echart对应的option代码
- echart-option模板中的title为表格名称，固定为‘登记状态’，无需更改
-  legend的中元素为表格中被投资企业的状态，你需要对表格中的所有企业的状态进行提取，并总结每个状态对应的被投资企业数量。
    - legend应该用圆点来做分割如下面这个格式：
    · 存续(23)                  37.50%
    · 注销(21)        20.83%
- 上面的格式23和21就是两个状态对应的被投资企业数量，另外其中37.50%和20.83%是该状态对应的被投资企业在整个表格中所占据的数量比例。
- series中的data每个元素的value值等于对应状态所有的被投资企业总数
- series中的data每个元素的value值总和要等于参考内容的被投资企业总数，务必保持相等
- 转换后的option要与模板风格和样式务必保持一致
- 数据总数要和参考内容一致（如：行数），不能擅自删除和修改数据，不能擅自删除和修改数据。

## 输出要求
- 把上面的数据转化为echart option代码
- 请不要输出别的内容,输出格式如下：
```json
{'option':'echarts的option代码内容'}
```
- ‘【’和‘】’符号包裹的是提示文字，不必输出该符号以及其包裹的提示文字。
- 再次强调，务必严格按模板转换要求进行转换，样式保持一致，输出内容务必按输出模板输出，不要包含其他内容和解释内容！不要包含其他内容和解释内容！
"""

# 投资地域
graph_outward_investment_investment_hell_template="""
# 角色
- 你是一个echart绘图专家

# 任务
- 基于‘参考内容’和‘要求’，帮我按要求生成echart相关代码。

# 模板
## echart模板
- 以下是echart对应的option模板：
【echart-option模板开始】
```json
{
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
}
```
【echart-option模板结束】

# 参考内容
【参考内容开始】
{context}
【参考内容结束】

# 要求

## 模板转换要求：
- 该模板在echart中对应的图表类型为：地图 
- 按照给定的echart-option模板，填补或替换模板中的数据，生成echart对应的option代码
- echart-option模板中的title为表格名称，固定为‘投资地域’，无需更改
- 你应该关注数据中“被投资企业的所属地区”，你只需要提取省份就行，以省份为单位进行分类，计算每个省份所对应的被投资企业数量，并在地图上进行标记，用颜色深浅来代表省份所包含公司的数量
- 图的左下角你应该标记颜色深浅对应不同数量的刻度标记。
- series中的data每个元素的value值等于对应地区所有的被投资企业总数
- 转换后的option要与模板风格和样式务必保持一致
- 数据总数要和参考内容一致（如：行数），不能擅自删除和修改数据，不能擅自删除和修改数据。

## 输出要求
- 把上面的数据转化为echart option代码
- 请不要输出别的内容,输出格式如下：
```json
{'option':'echarts的option代码内容'}
```
- ‘【’和‘】’符号包裹的是提示文字，不必输出该符号以及其包裹的提示文字。
- 再次强调，务必严格按模板转换要求进行转换，样式保持一致，输出内容务必按输出模板输出，不要包含其他内容和解释内容！不要包含其他内容和解释内容！
"""

graph_outward_investment_investment_trend_template="""
# 角色
- 你是一个echart绘图专家

# 任务
- 基于‘参考内容’和‘要求’，帮我按要求生成echart相关代码。

# 模板
## echart模板
- 以下是echart对应的option模板：
【echart-option模板开始】
```json
{
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
        1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1
      ],
    },
  ],
}
```
【echart-option模板结束】

# 参考内容
【参考内容开始】
{context}
【参考内容结束】

# 要求

## 模板转换要求：
- 该模板在echart中对应的图表类型为：地图 
- 按照给定的echart-option模板，填补或替换模板中的数据，生成echart对应的option代码
- echart-option模板中的title为表格名称，固定为‘投资趋势’，无需更改
- legend中只有‘投资数量’
- 并在图表下方要有一个滑动条，滑动该滚动条，图表中的年份区间也会随之改变，每滑动一次的区间大小为10年，滑动后展示该10年对外投资的数量趋势
- xAxis中的data代表年份，该年份属于‘参考内容’中‘成立日期’的所有年份，‘参考内容’中的所有年份信息你都应该写入到xAxis的data中，保证无数据缺失
- series中的data每个年份所对应的被投资企业总数。
- 转换后的option要与模板风格和样式务必保持一致
- 数据总数要和参考内容一致（如：行数），不能擅自删除和修改数据，不能擅自删除和修改数据。

## 输出要求
- 把上面的数据转化为echart option代码
- 请不要输出别的内容,输出格式如下：
```json
{'option':'echarts的option代码内容'}
```
- ‘【’和‘】’符号包裹的是提示文字，不必输出该符号以及其包裹的提示文字。
- 再次强调，务必严格按模板转换要求进行转换，样式保持一致，输出内容务必按输出模板输出，不要包含其他内容和解释内容！不要包含其他内容和解释内容！

"""