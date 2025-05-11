<template>
  <div class="app-container">
    <div style="margin-bottom:5px;font-weight:900">{{file_name}}</div>
    <el-form ref="queryForm" size="small" :inline="true">
        <el-form-item label="问题描述" prop="roleName">
          <el-input
            v-model="query"
            placeholder="请输入问题描述"
            clearable
            style="width: 240px"
            @keyup.enter.native="handleQuery"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
          <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :stripe="true" border :data="qaDataList" height="60vh">
        <el-table-column label="序号" align="center" type="index" width="50">
          <template slot-scope="scope">
            {{  scope.row.sort }}
          </template>
        </el-table-column>
        <el-table-column  label="问题" prop="question"/>
        <el-table-column label="答案" prop="answer" />
      </el-table>
  </div>
</template>

<script>
import { getQAList } from '@/utils/api/file';
export default {
    props:{
        file_name:{
            type:String,
            default:""
        },
        factory_name:{
            type:String,
            default:""
        },
        sort:{
            type:Number,
            default:-1
        }
    },
    data() {
        return {
            query:"",
            qaDataList:[]
        }
    },
    created(){
        this.initQAList()
    },
    methods:{
        initQAList(){
            if(this.file_name){
                this.$modal.loading("正在加载文件")
                getQAList({
                    file_name:this.file_name,
                    factory_name:this.factory_name,
                    sort:this.sort,
                    query:this.query
                }).then(res=>{
                    if(res && res.code && res.code===200){
                        this.qaDataList=res.data
                        console.log(this.qaDataList)
                    }
                }).finally(()=>{
                    this.$modal.closeLoading()
                })
            }
        },
        resetQuery(){
            this.query="",
            this.sort=-1
        },
        handleQuery(){
            this.initQAList()
        },
    },

    watch:{
        file_name(newVal){
            this.initQAList()
        },
        sort(newVal){
            this.initQAList()
        }
    }
}
</script>

<style>

</style>