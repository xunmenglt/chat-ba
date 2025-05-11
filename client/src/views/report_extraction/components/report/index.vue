<template>
    <el-dialog id="report" :visible.sync="dialogVisible" :fullscreen="true" :show-close="false">
        <template slot="title">
            <div class="index_search-item">
                <div class="index_search-item-left">
                    <img src="https://img5.tianyancha.com/logo/lll/5dba4af2ee162a87e085161393a3d47b.png@!f_200x200">
                </div>
                <div class="index_search-item-center">
                    <div class="index_header__x2QZ3">
                        <div class="index_name">
                            <a class="index_alink" href="https://www.tianyancha.com/company/8805958" target="_blank">
                                <span>{{gsxtInfo.qiye_name}}</span>
                            </a>

                            <el-tag type="success" size="mini">{{gsxtInfo.registration_status}}</el-tag>
                        </div>
                    </div>
                    <div class="index_tag-list-board">
                        <div class="index_tag-list">
                            <el-tag v-for="(tag) in good_tags" :key="tag" size="mini">{{tag}}</el-tag>
                            <el-tag v-for="(tag) in bad_tags" :key="tag" type="danger" size="mini">{{tag}}</el-tag>
                        </div>
                    </div>
                </div>
            </div>
            <div class="zhunrufen">
                <div class="one">98</div>
                <div class="two">准入分</div>
            </div>
        </template>
        <div class="info-container">
            <div class="info-block">
                <div class="block-title">
                    工商信息
                </div>
                <div class="block-content">
                    <el-descriptions class="margin-top" :column="3" border>
                        <el-descriptions-item :span="3">
                            <template slot="label">
                                企业名称
                            </template>
                            {{gsxtInfo.qiye_name}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                法定代表人
                            </template>
                            {{gsxtInfo.qiye_name}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                登记状态
                            </template>
                            {{gsxtInfo.registration_status}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                评分
                            </template>
                            98
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                成立日期
                            </template>
                            {{gsxtInfo.establishment_date}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                统一社会信用代码
                            </template>
                            {{gsxtInfo.credit_code}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                注册资本
                            </template>
                            {{gsxtInfo.registered_capital}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                实缴资本
                            </template>
                            {{gsxtInfo.capital_paid}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                工商注册号
                            </template>
                            {{gsxtInfo.business_number}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                纳税人识别号
                            </template>
                            {{gsxtInfo.taxpayer_number}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                组织机构代码
                            </template>
                            {{gsxtInfo.organization_code}}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                营业期限
                            </template>
                            {{ gsxtInfo.operating_term }}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                纳税人资质
                            </template>
                            {{ gsxtInfo.taxpayer_qualification }}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                核准日期
                            </template>
                            {{ gsxtInfo.approval_date }}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                企业类型
                            </template>
                            {{ gsxtInfo.enterprise_type }}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                行业
                            </template>
                            纺织业
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                人员规模
                            </template>
                            {{ gsxtInfo.personnel_size }}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                登记机关
                            </template>
                            {{ gsxtInfo.registration_authority }}
                        </el-descriptions-item>
                        <el-descriptions-item>
                            <template slot="label">
                                注册地址
                            </template>
                            {{ gsxtInfo.registered_address }}
                        </el-descriptions-item>
                        <el-descriptions-item :span="3">
                            <template slot="label">
                                经营范围
                            </template>
                            {{ gsxtInfo.business_scope }}
                        </el-descriptions-item>
                    </el-descriptions>
                </div>
            </div>
            <div class="info-block">
                <div class="block-title">
                    主要人员
                </div>
                <div class="block-content">
                    <el-table border :data="keyPersonsList" style="width: 100%">
                        <el-table-column prop="id" label="序号" width="180">
                        </el-table-column>
                        <el-table-column prop="name" label="姓名">
                        </el-table-column>
                        <el-table-column prop="position" label="职位">
                        </el-table-column>
                        <el-table-column prop="shareholding_ratio" label="持股比例">
                        </el-table-column>
                        <el-table-column prop="beneficial_share" label="最终受益股份">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
            <div class="info-block">
                <div class="block-title">
                    股东信息
                </div>
                <div class="block-content">
                    <el-table border :data="shareholderList" style="width: 100%">
                        <el-table-column prop="id" label="序号" width="180">
                        </el-table-column>
                        <el-table-column prop="name" label="股东名称">
                        </el-table-column>
                        <el-table-column prop="shareholding_ratio" label="持股比例">
                        </el-table-column>
                        <el-table-column prop="capital_contribution" label="认缴出资额(万元)">
                        </el-table-column>
                        <el-table-column prop="contribution_time" label="认缴出资日期">
                        </el-table-column>
                        <el-table-column prop="contribution_first" label="首次持股日期">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
            <div class="info-block">
                <div class="block-title">
                    对外投资分析
                </div>
                <div>
                    江苏阳光集团有限公司在多个行业和地区进行了广泛的投资，共涉及87家企业，其中大多数企业已经注销或吊销，只有少数企业目前处于存续状态。集团对多数企业的持股比例为<b
                        style="color: red">100%</b>，显示出其在这些企业中拥有完全的控制权。认缴出资额从<b style="color: red">几万元人民币</b>到<b
                        style="color: red">数亿元人民币</b>不等，投资的企业遍布江苏省多个城市，如江阴市、无锡市、南京市等，也有少数企业位于北京、上海、浙江等地。所属行业包括制造业、批发和零售业、科学研究和技术服务业、电力、热力、燃气及水生产和供应业等。

                </div>
                <div class="block-content">
                    <div class="chart-box-container">
                        <div class="chart-box">
                            <Chart :id="'11'" :option="investmentIndustryGraph" />
                        </div>
                        <div class="chart-box">
                            <Chart :id="'12'" :option="reistrationStatusGraph" />
                        </div>
                        <div class="chart-box">
                            <Chart :id="'13'" :option="investmentHellGraph" />
                        </div>
                        <div class="chart-box">
                            <Chart :id="'14'" :option="investmentTrendGraph" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="info-block">
                <div class="block-title">
                    司法案件
                </div>
                <div class="block-content">
                    <div class="chart-box-container right-content" style="height:200px">
                        <div class="content">
                            江苏阳光集团有限公司涉及的<strong>82</strong>条司法案件中，案件类型以<strong>民事案件</strong>为主，共<strong>72</strong>条，其中<strong>金融借款合同纠纷</strong>案件数量最多，为<strong>15</strong>条。公司在案件中主要身份为<strong>民事一审被告</strong>，出现<strong>49</strong>次，而作为<strong>原告</strong>的身份出现<strong>13</strong>次。审理程序大多处于<strong>民事一审</strong>阶段，且多数案件由<strong>江苏省无锡市中级人民法院</strong>审理。
                        </div>
                        <Chart :id="judicial_case_table.id" :option="judicial_case_table.option" />
                    </div>
                </div>
                <div>下面是前<strong>{{judicialCaseList.length}}</strong>条数据</div>
                <div class="block-content">
                    <el-table border :data="judicialCaseList" style="width: 100%">
                        <el-table-column prop="id" label="序号">
                        </el-table-column>
                        <el-table-column prop="judicial_name" label="案件名称">
                        </el-table-column>
                        <el-table-column prop="judicial_number" label="相关案号">
                        </el-table-column>
                        <el-table-column prop="cause" label="案由">
                        </el-table-column>
                        <el-table-column prop="type" label="案件类型">
                        </el-table-column>
                        <el-table-column prop="case_identity" label="案件身份">
                        </el-table-column>
                        <el-table-column prop="current_proceeding" label="当前审理程序">
                        </el-table-column>
                        <el-table-column prop="proceeding_date" label="当前审理程序日期">
                        </el-table-column>
                        <el-table-column prop="court" label="法院">
                        </el-table-column>
                    </el-table>
                </div>
                
            </div>
            <div class="info-block">
                <div class="block-title">
                    专利状况
                </div>
                <div>
                    江苏阳光集团有限公司自<strong>2001年</strong>起至<strong>2024年</strong>共申请了<strong>491项</strong>专利，其中<strong>2023年</strong>和<strong>2024年</strong>的申请最为活跃，专利类型主要为<strong>发明专利</strong>、<strong>外观专利</strong>和<strong>实用新型</strong>。专利状态显示，部分专利已获得<strong>授权</strong>，而有些则处于<strong>实质审查</strong>阶段，也有部分专利权已经<strong>终止</strong>。
                </div>
                <div class="block-content">
                    <div class="chart-box-container" style="height:300px">
                        <div class="chart-box">
                            <Chart :id="patent_activate_table.id" :option="patent_activate_table.option"/>
                        </div>
                        <div class="chart-box">
                            <Chart :id="patent_trend_table.id" :option="patent_trend_table.option" />
                        </div>
                    </div>
                </div>
                <div>下面是前<strong>{{patentList.length}}</strong>条数据</div>
                <div class="block-content">
                    <el-table border :data="patentList" style="width: 100%">
                        <el-table-column prop="id" label="序号" width="180">
                        </el-table-column>
                        <el-table-column prop="application_date" label="申请日期">
                        </el-table-column>
                        <el-table-column prop="patent_name" label="专利名称">
                        </el-table-column>
                        <el-table-column prop="patent_type" label="专利类型">
                        </el-table-column>
                        <el-table-column prop="patent_status" label="专利状态">
                        </el-table-column>
                        <el-table-column prop="application_id" label="申请号">
                        </el-table-column>
                        <el-table-column prop="inventor" label="发明人">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
            <div class="info-block">
                <div class="block-title">
                    报告总结
                </div>
                <div>
                    江苏阳光集团有限公司，成立于<strong>1993年7月17日</strong>，注册资本<strong>195,387.3万人民币</strong>，法定代表人为<strong>郁琴芬</strong>。公司类型为<strong>有限责任公司(自然人投资或控股)</strong>，所属行业为<strong>纺织业</strong>，目前处于<strong>存续</strong>状态。公司注册地址位于<strong>江阴市新桥镇陶新路18号</strong>，拥有<strong>39家分支机构</strong>，其中多数处于<strong>存续</strong>状态，少数已经<strong>注销</strong>或<strong>吊销</strong>。

公司经营范围广泛，包括但不限于面料纺织加工、纺纱加工、医疗器械生产与销售、软件开发、光伏设备制造与销售等。公司在<strong>2022年3月3日</strong>进行了经营范围的变更，增加了饮料生产、食品销售等项目。

在股东信息方面，<strong>江苏阳光控股集团有限公司</strong>持有<strong>99%</strong>的股份，<strong>郁琴芬</strong>持有<strong>1%</strong>的股份。法定代表人<strong>郁琴芬</strong>同时在<strong>15家企业</strong>担任法定代表人，并在<strong>18家企业</strong>中任职。

公司在知识产权方面表现活跃，拥有<strong>488件专利</strong>，包括发明专利、实用新型和外观专利，涉及服装制造、面料技术等多个领域。此外，公司还拥有<strong>100个注册商标</strong>，部分商标状态为<strong>“商标已注册”</strong>，而有些则显示为<strong>“商标无效”</strong>。

在风险信息方面，公司存在<strong>被执行人信息</strong>，涉及<strong>多起案件</strong>，执行标的总额高达数亿元。同时，公司也面临<strong>股权冻结</strong>的情况，涉及<strong>数千万人民币</strong>。

公司的财务数据显示，营业收入和净利润在不同年份有较大波动，总资产和净资产也呈现出一定的变化区间。公司的净利率和毛利率同样有所波动，显示出企业经营的不确定性。

总体来看，江苏阳光集团有限公司是一家在纺织业领域具有重要地位的企业，拥有多元化的业务和广泛的市场影响力。然而，公司也面临着一定的经营风险和法律问题，需要持续关注和妥善处理。

                </div>
            </div>
        </div>
        <span slot="footer" class="dialog-footer">
            <el-button size="mini" @click="dialogVisible = false">取 消</el-button>
            <el-button size="mini" type="warning" @click="downReport">下 载</el-button>
            <el-button size="mini" type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
    </el-dialog>
</template>

<script>
import { EventBus } from '@/utils/eventBus'
import Chart from '@/views/report_extraction/components/graph/chart.vue'
import IndexJS from './index.js'
import {
    getGsxtInfo,
    getKeyPersonsList,
    getShareholderList,
    getJudicialCaseList,
    getPatentList,
    getInvestmentIndustry,
    getRegistrationStatus,
    getInvestmentHell,
    getInvestmentTrend
} from '@/utils/api/report.js'
export default {
    components: { Chart },
    mixins: [IndexJS],
    data() {
        return {
            dialogVisible: false,
            credit_code:"",
            gsxtInfo:{},
            keyPersonsList:[],
            shareholderList:[],
            judicialCaseList:[],
            patentList:[],
            good_tags:[],
            bad_tags:[],
            investmentIndustryGraph:null,
            reistrationStatusGraph:null,
            investmentHellGraph:null,
            investmentTrendGraph:null
        }
    },
    created() {
        EventBus.$on("createReport", this.handleCreateReport)
    },
    methods: {
        handleCreateReport(credit_code) {
            // corporation_id公司ID
            this.dialogVisible = true
            this.credit_code=credit_code
        },
        async downReport() {
        },
        async flashGsxtInfo(){
            let result=await getGsxtInfo(this.credit_code)
            this.gsxtInfo=result.data
            let tags=this.gsxtInfo.tags
            if (tags){
                this.good_tags=tags.split("|")[0].split(",")
                this.bad_tags=tags.split("|")[1].split(",")
            }
            console.log(this.gsxtInfo)
        },
        async flashKeyPersonsList(){
            let result=await getKeyPersonsList(this.credit_code)
            this.keyPersonsList=result.data

        },
        async flashShareholderList(){
            let result=await getShareholderList(this.credit_code)
            this.shareholderList=result.data

        },
        async flashJudicialCaseList(){
            let result=await getJudicialCaseList(this.credit_code)
            this.judicialCaseList=result.data

        },
        async flashPatentList(){
            let result=await getPatentList(this.credit_code)
            this.patentList=result.data
        },
        async flashInvestmentIndustryGraph(){
            let result=await getInvestmentIndustry(this.credit_code)
            this.investmentIndustryGraph=result.data.option
        },
        async flashReistrationStatusGraph(){
            let result=await getRegistrationStatus(this.credit_code)
            this.reistrationStatusGraph=result.data.option
        },
        async flashInvestmentHellGraph(){
            let result=await getInvestmentHell(this.credit_code)
            this.investmentHellGraph=result.data.option
        },
        async flashInvestmentTrendGraph(){
            let result=await getInvestmentTrend(this.credit_code)
            this.investmentTrendGraph=result.data.option
        },
        randomUUID(){
            return String(new Date().getTime())
        }
    },
    watch:{
        async credit_code(newValue){
            if (newValue){
                await this.flashGsxtInfo()
                await this.flashKeyPersonsList()
                await this.flashShareholderList()
                await this.flashJudicialCaseList()
                await this.flashPatentList()
                await this.flashInvestmentIndustryGraph()
                await this.flashReistrationStatusGraph()
                await this.flashInvestmentHellGraph()
                await this.flashInvestmentTrendGraph()
            }
        }
    }
}
</script>

<style lang="less" scoped>
.index_search-item {
    height: 60px;
    position: relative;
    padding: 16px 20px;
}

.index_search-item {
    display: flex;
}

.index_search-item-left {
    position: relative;
    width: 60px;
    margin-right: 25px;
    display: flex;
    align-items: center;

    img {
        width: 100%;
    }
}

.create-report-container {
    position: absolute;
    right: 10px;
    bottom: 10px;
}

.block-content {
    width: 100%;
}

.block-title {
    font-weight: 900;
}

.chart-box-container {
    width: 100%;
    position: relative;
}

.chart-box {
    width: 48%;
    display: inline-block;
    height: 300px;
    position: relative;
    margin: auto;
}
strong{
    color: red;
}
b{
    color: red;
}
.right-content{
    display: flex;
    height: 300px;
    align-items: center;
    justify-content: space-between;
    .content{
        width: 30%;
    }
}
.zhunrufen{
    position: absolute;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    left: 90%;
    top: 5%;
    display: flex;
    .one,.two{
        font-size: 20px;
        font-weight: 600;
    }
    .one{
        color: rgb(0, 179, 255);
    }
    .two{
        color: #b1b1b1;
    }
}
</style>