<template>
    <div class="card-contaienr">

        <div class="index_search-item">
            <div class="index_search-item-left">
                <img :src="qiye.logo">
            </div>
            <div class="index_search-item-center">
                <div class="index_header__x2QZ3">
                    <div class="index_name">
                        <a class="index_alink"
                            href="https://www.tianyancha.com/company/8805958"
                            target="_blank">
                            <span>{{ qiye.qiye_name }}</span>
                        </a>
                    </div>
                    <el-tag type="success" size="mini">{{ qiye.registration_status }}</el-tag>
                </div>
                <div class="index_tag-list-board">
                    <div class="index_tag-list">
                        <el-tag v-for="(tag) in good_tags" :key="tag" size="mini">{{tag}}</el-tag>
                        <el-tag v-for="(tag) in bad_tags" :key="tag" type="danger" size="mini">{{tag}}</el-tag>
                    </div>
                </div>
                <div class="index_info-row index_info-row-wrap">
                    <div class="index_info-col index_wider">
                        法定代表人：
                        <a class="link-click"
                            href="https://www.tianyancha.com/human/2333988423-c8805958"
                            target="_blank">
                            <span>{{qiye.legal_representative}}</span>
                        </a>
                    </div>
                    <div class="index_info-col">
                        注册资本：
                        <span class="index_value">{{qiye.capital_paid}}</span>
                    </div>
                    <div class="index_info-col">
                        成立日期：
                        <span class="index_value">{{qiye.establishment_date}}</span>
                    </div>
                    <div class="index_info-col index_credit-code">
                        统一社会信用代码：
                        <span class="index_value">{{qiye.credit_code}}</span>
                    </div>
                </div>
                <div class="index_contact-row">
                    <div class="index_contact-col index_address">
                        <span class="index_label">地址：</span>
                        <span class="index_value">
                            {{qiye.registered_address}}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <div class="create-report-container">
            <el-button @click="createReport" icon="el-icon-document" size="mini" plain type="primary">报告</el-button>
        </div>

    </div>
</template>

<script>
import { EventBus } from '@/utils/eventBus'
export default {
    props:{
        qiye:{
            type:Object,
            default:()=>{}
        }
    },
    data() {
        return {
            good_tags:[],
            bad_tags:[]
        }
    },
    created(){
        let tags=this.qiye.tags
        if (tags){
            this.good_tags=tags.split("|")[0].split(",")
            this.bad_tags=tags.split("|")[1].split(",")
        }
    },
    methods:{
        createReport(){
            EventBus.$emit("createReport",this.qiye.credit_code)            
        }
    }
}
</script>

<style lang="less" scoped>
.card-contaienr {
    min-height: 126px;
    position: relative;
    padding: 16px 20px;
}

.index_search-item {
    display: flex;
    width: 920px;

}

.index_search-item-left {
    position: relative;
    width: 88px;
    margin-right: 25px;
    display: flex;
    align-items: center;

    img {
        width: 100%;
    }
}
.create-report-container{
    position: absolute;
    right: 10px;
    bottom: 10px;
}
</style>