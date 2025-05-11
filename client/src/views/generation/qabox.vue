<template>
  <div class="qabox-container">
    <div :class="['qabox-top',canSend?'nothit':'']">
        <div class="qabox-top-left">
            <div class="controller-item">
                <div class="controller-label">
                    模型名称:
                </div>
                <div class="controller-compoment">
                    <el-select size="mini" v-model="model_name"  placeholder="请选择模型">
                        <el-option v-for="model in modelList" :key="model" :label="model" :value="model"></el-option>
                    </el-select>
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    prompt名称:
                </div>
                <div class="controller-compoment">
                    <el-select size="mini" v-model="prompt_name"  placeholder="请选择prompt">
                        <el-option v-for="prompt in promptList" :key="prompt" :label="prompt" :value="prompt"></el-option>
                    </el-select>
                    <el-popover
                        placement="bottom"
                        title="模板内容"
                        trigger="click"
                        width="400">
                        <div style="white-space:pre-wrap;" >{{promptInfo}}</div>
                        <el-button size="mini" slot="reference" type="text" @click="toGetPromptInfo"><i class="el-icon-view"></i>查看模板</el-button>
                    </el-popover>
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    输入方式:
                </div>
                <div class="controller-compoment">
                    <el-radio-group  v-model="query_type">
                        <el-radio  :label="'input'">手动</el-radio>
                        <el-radio  :label="'file'">文件</el-radio>
                    </el-radio-group>
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    是否切分:
                </div>
                <div class="controller-compoment">
                    <el-radio-group  v-model="do_split">
                        <el-radio  :label="true">是</el-radio>
                        <el-radio  :label="false">否</el-radio>
                    </el-radio-group>
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    生成数目:
                </div>
                <div class="controller-compoment">
                    <el-input-number size="mini" class="item" v-model="qa_count" :min="1" :max="100"></el-input-number>
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    输入内容:
                </div>
                <div class="controller-compoment">
                    <el-input
                        type="textarea"
                        placeholder="请输入内容"
                        v-model="input"
                        maxlength="1024"
                        show-word-limit
                        rows="1"
                    >
                    </el-input>
                </div>
            </div>
        </div>
        <div class="qabox-top-right">
            <div class="item">
                <el-button size="mini" type="primary" :disabled="canSend" @click="doGenerationQA">{{btn_tip}}</el-button>
            </div>
            <div class="item">
                <el-button size="mini" type="danger" icon="el-icon-delete" @click="deleteItem" circle></el-button>
            </div>
        </div>
    </div>
    <div class="qabox-center">
        <el-progress v-if="canSend" :percentage="Math.ceil((qaDataList.length/qa_count)*100)"></el-progress>
        <el-table @selection-change="handleSelectionChange" :stripe="true" border :data="qaDataList">
            <el-table-column
                type="selection"
                width="55">
            </el-table-column>
            <el-table-column label="序号" align="center" type="index" width="50">
              <template slot-scope="scope">
                {{  scope.row.index }}
              </template>
            </el-table-column>
            <el-table-column  label="问题" prop="question"/>
            <el-table-column label="答案" prop="answer" />
            <el-table-column label="文件名称" prop="filename" />
            <el-table-column label="质量分数" prop="score" />
        </el-table>
    </div>
    <div class="qabox-footer">
        
        <div class="qabox-footer-left">
            <div class="controller-item">
                <div class="controller-label">
                    数据数量:
                </div>
                <div class="controller-compoment">
                    {{ qaDataList.length }}
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    重试次数:
                </div>
                <div class="controller-compoment">
                    {{ try_count }}
                </div>
            </div>
            <div class="controller-item">
                <div class="controller-label">
                    质量分数:
                </div>
                <div class="controller-compoment">
                    <span style="color: red;">{{ quality_score }}</span>
                </div>
            </div>
        </div>
        <div class="qabox-footer-right">
            <el-button size="mini" v-if="qaDataList&&qaDataList.length>0&&!canSend" @click="evalQAScore" type="primary">评分</el-button>
            <el-button size="mini" type="primary" v-if="!canSend&&current_file_id" @click="downLoadQAFile()"><i class="el-icon-download el-icon--left"></i>下载文件</el-button>
        </div>
    </div>    
  </div>
</template>

<script>
import { QAGeneration } from '@/utils/api/chat'
import { getModelList } from '@/utils/api/model'
import { getPromptList,getPromptInfo } from '@/utils/api/prompt.js'
import { downLoadQAFileAPI, getEvalQAScore } from '@/utils/api/generation'

export default {
    props:{
        upload_id:{
            type:String,
            default:""
        },
        file_name:{
            type:String,
            default:""
        },
        qa_box_id:{
            type:String,
            default:"",
        }
    },
    data() {
        return {
            // 输入内容
            input:"",
            // 查询类型
            query_type:"file",
            // 生成问答对数量
            qa_count:3,
            // 模板名称
            prompt_name:"default",
            // 文本最大生成数
            max_tokens:2048,
            // 模型名称
            model_name:"",
            //温度
            temperature:0.2,
            // top_p
            top_p:0.9,
            quality_score:-1,
            try_count:-1,
            // qa问答对数据
            qaDataList:[],
            // 模型列表
            modelList:[],
            // prompt列表
            promptList:[],
            promptInfo:"",
            canSend:false,
            btn_tip:"开始生成",
            do_split:false,
            current_file_id:"",
            current_qa_ids:"",
            geneation_stype:{
                0:"表示开始生成",
                2:"生成的答案",
                3:"生成结束",
                4:"异常",
                5:"重试次数"
            },
        }
    },
    created(){
        this.initModelList(),
        this.initPromptList()
    },
    methods:{
        deleteItem(){
            this.$emit('deleteItem',this.qa_box_id)
        },
        downLoadQAFile(){
            downLoadQAFileAPI({
                qa_box_id:this.qa_box_id,
                file_id:this.current_file_id,
                qa_ids:this.current_qa_ids,
                file_name:this.file_name
            })
        },
        createGenerationParam(){
            return {
                "input": this.input,
                "top_p": this.top_p,
                "temperature": this.temperature,
                "model_name": this.model_name,
                "max_tokens": this.max_tokens,
                "prompt_name": this.prompt_name,
                "query_type": this.query_type,
                "upload_id": this.upload_id,
                "file_name": this.file_name,
                "qa_count": this.qa_count,
                "qa_box_id":this.qa_box_id,
                "do_split":this.do_split
            }
        },
        flashTableScroll() {
            this.$nextTick(() => { // 确保DOM已经更新完成
                const container = document.querySelector(".el-table__body-wrapper");
                if (container) {
                    container.scrollTop = container.scrollHeight - container.clientHeight;
                }
            });
        },
        initModelList() {
            let that =this
            getModelList().then(res => {
                this.modelList = res.data
                if (this.modelList.length > 0) {
                    this.model_name = this.modelList[0]
                }
            }).catch(e => {
                that.$modal.msgError("获取模型列表异常")
            })
        },
        initPromptList(){
            getPromptList({type:"generation"}).then(res => {
                this.promptList = res.data
                if(this.promptList.length>0){
                this.prompt_name=this.promptList[0]
                }
            }).catch(e => {
                this.$modal.msgError("获取模板列表异常")
            })
        },
        toGetPromptInfo(){
            getPromptInfo({type:"generation",prompt_name:this.prompt_name}).then(res => {
                this.promptInfo = res.data
            }).catch(e => {
                this.$modal.msgInfo(TYPE.ERROR, `获取模板【${this.require_data.prompt_name}】信息异常`)
            })
        },
        readCallback(isfirst,chunkValue){
            let data_object = null
            try {
                data_object = JSON.parse(chunkValue.substring("data:".length, chunkValue.length).trim())
            } catch (error) {
                return
            }
            console.log(data_object)
            if(data_object["flag"]!= undefined){
                let flag=data_object["flag"]
                let answer=data_object["answer"]
                if (flag===0){
                    // 开始生成
                    this.$modal.msgWarning("开始生成数据")
                    this.btn_tip="生成中"
                    this.canSend=true
                }else if(flag===2){
                    //生成的答案
                    let qa=answer.data
                    qa.index=answer.index
                    qa.score=-1
                    this.qaDataList=[...this.qaDataList,qa]
                    this.flashTableScroll()
                }else if(flag===3){
                    //生成结束
                    this.$modal.msgSuccess("生成完毕")
                    this.canSend=false
                    this.btn_tip="开始生成"
                }else if(flag===4){
                    //异常
                    this.$modal.msgError(answer["msg"])
                    this.btn_tip="开始生成"
                    this.canSend=false
                }else if(flag===5){
                    //重试次数
                    this.try_count=answer.max_try
                }else if(flag===6){
                    //文件下载id
                    this.current_file_id=answer.data.file_id
                }
            }
        },
        endCallback(){
            this.canSend=false
        },
        doGenerationQA(){
            this.canSend=false
            this.qaDataList=[]
            let data=this.createGenerationParam()
            QAGeneration(data,
                this.readCallback,
                this.endCallback
            )
        },
        evalQAScore(){
            let qa_box_id=this.qa_box_id
            let file_id=this.current_file_id
            this.$modal.loading("正在评分,请等待")
            getEvalQAScore(qa_box_id,file_id).then((res)=>{
                if (res && res.code && res.code===200){
                    // 每个问答对的分数
                    let qa_every_score=res.data.qa_every_score
                    // 获取平均分
                    this.quality_score=res.data.average
                    for(let i=0;i<this.qaDataList.length;i++){
                        this.qaDataList[i].score=qa_every_score[i]
                    }
                }else{
                    this.$modal.msgError(res.msg)
                }
            }).finally(()=>{
                this.$modal.closeLoading()
            })
        },
        handleSelectionChange(ids){
            this.current_qa_ids=ids.map((e)=>e.index)
        }
    }
}
</script>

<style lang="less" scoped>
/* 整个滚动条 */
 /deep/ .el-table__body-wrapper::-webkit-scrollbar {
    width: 5px;
    /* 滚动条的宽度 */
    height: 10px;
    /* 滚动条的高度，对水平滚动条有效 */
    position: absolute;
  }
  
  /* 滚动条轨道 */
  /deep/ .el-table__body-wrapper::-webkit-scrollbar-track {
    border-radius: 10px;
  }
  
  /* 滚动条滑块 */
  /deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background-color: #c1c1c1;
    /* 滑块的背景颜色 */
    border: 3px solid #e1e1e1;
    /* 滑块的边框和轨道相同的颜色，可以制造“边距”的效果 */
  }
  
  /deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb:hover {
    background-color: #d4d4d4;
    /* 滑块的悬停颜色 */
  }
  
  /deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb:active {
    background-color: #d3d3d3;
    /* 滑块的激活颜色 */
  }
  .nothit{
    pointer-events: none;
    opacity: 0.5;
  }
  .qabox-top{
    display: inline-flex;
    justify-content: space-between;
    width: 100%;
    padding: 0 2px 0 2px;
    transition: opacity 0.5s ease;
    .qabox-top-left{
        display: inline-flex;
        flex-wrap: wrap;
    }
  }
  .controller-item{
    display: flex;
    align-items: center;
    margin-bottom: 2px;
    .controller-label{
        font-size: 10px;
        font-weight: 900;
        text-align: right;
        width: 70px;
        margin-right: 2px;
    }
    .controller-compoment{
        font-size: 10px;
    }
  }
  /deep/ .el-table__body-wrapper{
    height: 50vh;
    overflow-y: auto;
  }
  .qabox-footer{
    display: inline-flex;
    justify-content: space-between;
    padding: 0 5px 0 5px;
    width: 100%;
    margin-top: 5px;
    .qabox-footer-left{
        display: inline-flex;
    }
  }
  /deep/ .el-radio__inner{
    width: 10px;
    height: 10px;
  }
  /deep/ .el-radio__label{
    font-size: 10px;
  }
  /deep/ .el-radio {
    margin-right: 10px;
  }
  .qabox-top-right{
    display: flex;
    padding: 0 10px 0 10px;
    align-items: center;
    .item{
        margin-right: 5px;
    }
  }
</style>