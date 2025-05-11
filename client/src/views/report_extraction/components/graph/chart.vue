<template>
    <div class="chart-container">
        <el-skeleton class="skeleton" v-if="!chart" :rows="6" animated />
        <div :id="id" style="width:100%;height:100%"></div>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import '@/assets/js/china.js'

export default {
    props: {
        id: {
            type: String,
            default: ""
        },
        option: {
            type: Object,
            default: ()=>{}
        },
    },
    data() {
        return {
            canShow: false,
            chart: null,
        }
    },
    methods: {
        renderCharts() {
            setTimeout(() => {
                this.chart = echarts.init(document.getElementById(this.id))
                this.chart.clear()
                this.chart.setOption(this.option)
                // 将图表自适应窗口大小
                window.addEventListener("resize",  ()=>{
                    this.chart.resize();
                });
            },3000+Math.floor(Math.random()*1000))
        }
    },
    created(){
        if(this.id && this.option!=null){
            this.renderCharts()
        }
    },
    watch:{
        option(newValue){
            if (newValue && newValue!=null && newValue!=undefined){
                this.renderCharts()
            }
        }
    }
}
</script>

<style>
.chart-container {
    width: 100%;
    height: 100%;
    margin: 0;
    position: relative;
}
</style>