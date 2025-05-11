<template>
  <div class="content-container">
    <div class="top-div">
      <div class="serach-box">
        <el-input type="textarea" :rows="1" resize="none" placeholder="输入公司名称、老板姓名、品牌名称">
        </el-input>
        <div class="opt-item">
          <i class="icon el-icon-search"></i>
        </div>
      </div>
    </div>
    <div class="qiyecard_item" v-for="item in searchDataList" :key="item.credit_code">
      <SearchCard :qiye="item" />
    </div>
    <Report />
  </div>
</template>

<script>
import SearchCard from './components/corporation/searchcard.vue'
import Report from './components/report/index.vue'
import {getIndexList} from '@/utils/api/report.js'
export default {
    components:{SearchCard,Report},
    data() {
      return {
        searchDataList:[],
        page_number:1,
        page_size:10
      }
    },
    created(){
      this.flash_data_list()
    },
    methods:{
      async flash_data_list(){
        let result=await getIndexList()
        this.searchDataList=result.data
      }
    }
}
</script>

<style lang="less" scoped>
.content-container{
  overflow-y: auto;
  padding: 0 50px 0 50px;
}
.qiyecard_item{
  margin-top: 5px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.serach-box{
  width: 600px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  display: flex;
  background: #e6063e;
  padding: 12px 12px 12px 16px;
  border-radius: 24px;
  .opt-item{
      width: 24px;
      height: 26px;
      color: #fff;
      font-size: 18px;
      margin-left: 10px;
  }
}
/deep/ textarea{
  border: none;
}
/deep/ .el-form-item{
  display: flex;
  .el-form-item__content{
      flex: 1;
  }
  .el-form-item__label{
      width: 100px;
  }
}
.input-focus{
  border: 1px solid #4d53e8;
}
.top-div{
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>