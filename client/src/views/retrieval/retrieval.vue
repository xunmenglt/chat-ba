<template>
  <div class="content-container">
    <el-drawer title="设置" :visible.sync="showSetting" :direction="'ltr'" size="30%">
      <div class="add-container">
        <el-form  size="mini" :inline="true">
          <el-form-item label="知识库：">
            <el-select @change="changeFactory" v-model="require_data.factory_name"  placeholder="请选择知识库">
              <el-option v-for="item in factoryList" :key="item.id" :label="item.kb_info" :value="item.kb_name"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div class="conversation-list-container">
        <div :class="['win-item']" v-for="file in fileList"
          :key="file.id">
          <div class="win-item-wrap">
            <div class="win-item-title">
              <span style="margin-right: 4px;">
                <v-icon>
                  mdi-file-document
                </v-icon>
              </span>
              <span class="chat-history-message">
                {{ file.file_name }}
              </span>
            </div>
          </div>

          <div class="his-action">
            <div class="action-item action-item-delete" @click.stop="toViewFile(file)">
              <v-icon style="  color: green;">
                mdi-eye
              </v-icon>
            </div>
          </div>
        </div>
      </div>
      <div class="option-container">
        <div><v-select :items="modelList" solo v-model="require_data.model_name" label="请选择模型*" required></v-select>
        </div>
        <v-btn class="ma-2 more-btn" color="info" @click.stop="showHightSetting = true">
          <v-icon dark>
            mdi-wrench
          </v-icon>
          高级操作
        </v-btn>
      </div>
      <el-drawer title="高级操作" :width="400" :append-to-body="true" :visible.sync="showHightSetting">
        <div class="controller-container">
          <div class="controller-item">
            <div class="controller-label">
                模板名称:
            </div>
            <div class="controller-compoment" style="padding-right:5px">
                <el-select  v-model="require_data.prompt_name" clearable placeholder="请选择">
                  <el-option
                    v-for="item in promptList"
                    :key="item"
                    :label="item"
                    :value="item">
                  </el-option>
                </el-select>
            </div>
              <el-popover
              placement="bottom"
              title="模板内容"
              trigger="click"
              width="400">
              <div style="white-space:pre-wrap;" >{{promptInfo}}</div>
              <el-button slot="reference" type="text" @click="toGetPromptInfo"><i class="el-icon-view"></i>查看模板</el-button>
          </el-popover>
        </div>
            <div class="controller-item">
              <div class="controller-label">
                  文档匹配数:
              </div>
              <div class="controller-compoment">
                  <el-input-number class="item" v-model="require_data.top_k" :min="0" :max="5"></el-input-number>
              </div>
          </div>
            <div class="controller-item">
              <div class="controller-label">
                  相似阈值:
              </div>
              <div class="controller-compoment">
                  <el-slider class="item" v-model="score_threshold" :format-tooltip="formatScore_threshold"></el-slider>
              </div>
          </div>
          <div class="controller-item">
              <div class="controller-label">
                  temperature:
              </div>
              <div class="controller-compoment">
                  <el-slider class="item" v-model="temperature" :format-tooltip="formatTemperature"></el-slider>
              </div>
          </div>
          <div class="controller-item">
            <div class="controller-label">
                top_p:
            </div>
            <div class="controller-compoment">
                <el-slider class="item" v-model="top_p" :format-tooltip="formatTop_p"></el-slider>
            </div>
          </div>
          <div class="controller-item">
              <div class="controller-label">
                  max_tokens:
              </div>
              <div class="controller-compoment">
                  <el-slider class="item" v-model="max_tokens" :format-tooltip="formatMax_tokens"></el-slider>
              </div>
          </div>
          <div class="controller-item">
            <div class="controller-label">
                流式输出:
            </div>
            <div class="controller-compoment">
              <el-radio-group v-model="require_data.stream">
                <el-radio :label="true">是</el-radio>
                <el-radio :label="false">否</el-radio>
              </el-radio-group>
            </div>
        </div>
      </div>
      </el-drawer>

    </el-drawer>


    <!-- 对话窗口 -->
    <div class="concersation-container">
      <div class="message-container" ref="scrollContainer">
        <div v-for="(message, index) in messageList" :key="index">
          <div v-if="message['query']" class="human_message-container">
            <div class="human-message">{{ message['query'] }}</div>
            <div class="human-logo">
              <img :src="PersonImage">
            </div>
          </div>
          <div v-if="message['response']" class="ai-message-container">
            <div class="ai-logo">
              <img :src="RobotImage">
            </div>
            <div class="ai-message">
              <messageVue :value="message['response']" />
              <div class="recommend">
                <div class="recommend-file">
                  <div class="docItem fileItem" 
                  @click="toViewFile(file)"
                  v-for="(file,index) in message['file_docs']" :key="index">
                    <i class="mdi mdi-file-document">
                    </i>
                    {{ file.file_name }}
                  </div>
                </div>
                <div class="recommend-qa">
                  <div class="docItem qaItem" 
                  @click="toViewFile(qa)"
                  v-for="(qa,index) in message['qa_docs']" :key="index">
                    <i class="icon el-icon-question">
                    </i>
                    {{ qa.question }}
                  </div>
                </div>
              </div>
            </div>
            <v-progress-circular v-if="message['is_sending']" indeterminate color="primary"
              :size="20"></v-progress-circular>
          </div>
        </div>
      </div>
      <div class="submit-container">
        <!-- <div class="recommend-container" v-if="docs && docs.length>0">
          <div class="prefix-desc">推荐内容：</div>
          <div class="tip-desc">
            <div class="tip-item" v-for="(item,index) in docs" :key="index">
              {{ item.file_name }}
            </div>
          </div>
        </div> -->
        <div class="text-container">
          <el-input :disabled="!canSend" type="textarea" maxlength="1024" show-word-limit resize="none" :rows="4"
            placeholder="在此输入您的问题，Ctrl+Enter发送。" v-model="require_data.query">
          </el-input>
        </div>
        <div class="btn-container">
          <el-tooltip class="item" effect="dark" content="点击打开设置，可更改对话、变量等" placement="right-start">
            <el-button size="mini" type="info" circle @click="showSetting = true">
              <v-icon dark>
                mdi-wrench
              </v-icon>
            </el-button>
          </el-tooltip>
          <el-button type="primary" :disabled="!canSend" icon="el-icon-chat-dot-round" round
            @click="handlerSendMessage">发送</el-button>
        </div>
      </div>
    </div>
    <!-- 文档预览 -->
    <el-dialog v-loading="rending" top="10px" title="文档预览" :visible.sync="isRenderFile" width="60%" :close-on-click-modal="false">
      <div style="height: 70vh">
        <Qaview v-if="renderFileType==4" :file_name="currentFile.file_name"
        :factory_name="currentFile.kb_name||currentFile.factory_name"
        :sort="qa_sort"/>
        <iframe v-if="renderFileType==1" style="width: 100%;height:100%" :src="renderFileSrc"></iframe>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import RobotImage from '@/assets/icons/robot.png'
import PersonImage from '@/assets/icons/person.png'
import messageVue from '@/components/message/message.vue'
import { getKnowledgeBaseListApi} from '@/utils/api/knowledgebase'
import { getKnowledgeFileListApi} from '@/utils/api/knowledgedoc'
import {getFileSrc} from '@/utils/api/file'
import { getModelList } from '@/utils/api/model.js'
import { getPromptList,getPromptInfo } from '@/utils/api/prompt.js'
import { showTextMessage } from '@/plugins/toastification'
import { TYPE } from 'vue-toastification'
import {RetrievalChat} from '@/utils/api/chat'
import Qaview from '@/components/qaview/index.vue'
export default {
  components: { messageVue,Qaview},
  data() {
    return {
      temperature:95,
      top_p:90,
      max_tokens:50,
      factoryList:[],
      score_threshold:70,
      require_data: {
        "query": "",
        "factory_name":"",
        "top_k": 5,
        "top_p":0.9,
        "score_threshold": 0.5,
        "stream": true,
        "model_name": "",
        "temperature": 0.7,
        "max_tokens": 1024,
        "prompt_name": "default"
      },

      PersonImage: PersonImage,
      RobotImage: RobotImage,
      modelList: [],
      promptList:[],
      promptInfo:"",
      activateId: "",
      showSetting: false,
      showHightSetting: false,
      canSend: true,
      winList: [],
      // 当前文件
      currentFile:{},
      qa_sort:-1,
      currentReplayMessage:{},
      docs:[],
      fileList:[],
      fileListLoadding:false,
      messageList: [
      ],
      renderFileType:-1,
      isRenderFile:false,
      renderFileSrc:"",
      rending:false,
      editorOptions:{
        toolbar: true,
      }
    }
  },
  mounted(){
    window.addEventListener("keydown", this.quickSend, false);
  },
  destroyed(){
    window.removeEventListener("keydown", this.quickSend);
  },
  created() {
    this.initFactoryList()
    this.initModelList()
    this.initPromptList()
  },
  
  methods: {
    initFactoryList(){
      getKnowledgeBaseListApi().then(res => {
        this.factoryList = res.data
        if(this.factoryList.length>0){
          this.require_data.factory_name=this.factoryList[0].kb_name
          this.changeFactory()
        }
      }).catch(e => {
        showTextMessage(TYPE.ERROR, "获取知识库列表异常")
      })
    },
    initModelList(){
      getModelList().then(res => {
        this.modelList = res.data
        if(this.modelList.length>0){
          this.require_data.model_name=this.modelList[0]
        }
      }).catch(e => {
        showTextMessage(TYPE.ERROR, "获取模型列表异常")
      })
    },
    initPromptList(){
      getPromptList({type:"retrieval"}).then(res => {
        this.promptList = res.data
        if(this.promptList.length>0){
          this.require_data.prompt_name=this.promptList[0]
        }
      }).catch(e => {
        showTextMessage(TYPE.ERROR, "获取模板列表异常")
      })
    },
    toGetPromptInfo(){
      getPromptInfo({type:"retrieval",prompt_name:this.require_data.prompt_name}).then(res => {
        this.promptInfo = res.data
      }).catch(e => {
        showTextMessage(TYPE.ERROR, `获取模板【${this.require_data.prompt_name}】信息异常`)
      })
    },
    toViewFile(file) {
      if (file){
        this.renderFileType=-1
        this.isRenderFile=true
        this.$modal.loading("正在加载文件")
        this.currentFile=file
        console.log(this.currentFile)
        if(file.file_ext.indexOf('pdf')>=0){
          // 预览pdf
          this.renderFileType=1
          this.renderFileSrc=getFileSrc(file.id)
        }else if(file.file_ext.indexOf('doc')>=0) {
          // 预览doc
          this.renderFileType=2
        }else if(file.file_ext.indexOf('xls')>=0){
          // 预览xls
          this.renderFileType=3
        }else{
          if(file.sort>=0){
            this.qa_sort=file.sort
          }
          this.renderFileType=4
        }
      }else{
        this.$modal.msgWarning("文件不存在")
      }
      this.$modal.closeLoading()
    },
    fileRendered(){
      this.rending=false
    },
    fileErrorHandler(e){
      console.log(e)
      this.rending=false
      if(this.renderFileType==2){
        this.$modal.msgWarning("暂不支持word渲染")
      }
    },
    changeFactory() {
      this.fileListLoadding=true
      if(this.require_data.factory_name){
        getKnowledgeFileListApi({factory_name:this.require_data.factory_name}).then(res=>{
        this.fileList=res.data
      }).catch(e=>{
      }).finally(_=>{
        this.fileListLoadding=false
      })
      }
    },
    // 处理信息
    flashScroll() {
      this.$nextTick(() => { // 确保DOM已经更新完成
        const container = this.$refs.scrollContainer;
        if (container) {
          container.scrollTop = container.scrollHeight - container.clientHeight;
        }
      });
    },
    quickSend(e){
      let that=this
      if (e.ctrlKey && e.keyCode==13){
          that.handlerSendMessage()
      }   
    },
    handlerSendMessage() {
      if (!this.require_data.factory_name){
        // 创建新的对话框
        this.$modal.msgWarning("请选择知识库")
        return
      }
      this.doSendMessage()
    },
    doSendMessage(){
      if (this.canSend && this.require_data.query){
        this.canSend=false
        let newMessage={
          query:this.require_data.query+'',
          response:'',
          file_docs:[],
          qa_docs:[],
          is_sending:true,
        }
        this.messageList.push(newMessage)
        this.currentReplayMessage=newMessage
        this.flashScroll()
        console.log(this.require_data)
        RetrievalChat(this.require_data,
          this.readCallback,
          this.endCallback
        )
      }
    },
    readCallback(isfirst,chunkValue){
      let data_object = null
      try {
        data_object = JSON.parse(chunkValue.substring("data:".length, chunkValue.length).trim())
      } catch (error) {
        return
      }
      if (data_object["answer"]) {
        let text = data_object["answer"]
        this.currentReplayMessage.response+=text
      }
      if (data_object["docs"] != undefined) {
        let docs=data_object["docs"]
        if (docs){
          console.log(docs)
          docs.forEach(doc => {
            if(doc.file_ext && doc.file_ext.indexOf('.json')!=-1){
              this.currentReplayMessage.qa_docs.push(doc)
            }else{
              this.currentReplayMessage.file_docs.push(doc)
            }
          });
        }
      }
      this.flashScroll()
    },
    endCallback(){
      this.currentReplayMessage.is_sending=false
      this.canSend=true
      this.require_data.query=""
    },
    // 格式化
    formatTemperature(val) {
      let value = val / 100
      this.require_data.temperature = value
      return value
    },
    formatTop_p(val) {
      let value = val / 100
      this.require_data.top_p = value
      return value
    },
    formatMax_tokens(val) {
      let value = Math.floor(val * (1024 / 100))
      this.require_data.max_tokens = value
      return value
    },
    formatScore_threshold(val){
                let value= val/100
                this.require_data.score_threshold=value
                return value
    },
  }
}
</script>

<style lang="less" scoped>

.add-container {
  width: 100%;
  height: 48px;
  border-bottom: 2px solid #aaaaaa;
  align-items: center;
  justify-content: center;
  display: flex;
  padding: 0 5px;
  /deep/ .el-form-item{
    margin-bottom: 0;
  }
  /deep/ .el-form-item__label{
    font-weight: 900;
  }
  .add-btn {
    width: 100%;
  }
}

.conversation-list-container {
  height: calc(100% - 200px);
  padding: 2px 5px;
  overflow-y: auto;
}

.option-container {
  width: 100%;
  border-top: 2px solid #aaaaaa;
  position: absolute;
  bottom: 0;
  height: 148px;
  padding: 0 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .more-btn {
    width: 100%;
  }
}

.v-navigation-drawer__content {
  position: relative;
}


.win-item-wrap {
  min-width: 0;
  width: 100%;
}

.win-item-title {
  display: flex;
  align-items: center;
  position: relative;
}

.win-item {
  height: 42px;
  border-radius: 12px;
  margin-bottom: 4px;
  font-size: 14px;
  box-sizing: border-box;
  cursor: pointer;
  line-height: 42px;
  padding: 0 5px;
  position: relative;
}

.win-item:hover {
  background: #d7f6ff;
  box-shadow: 0 2px 6px #0000001a;

  .his-action {
    display: block;
  }
}

.his-action {
  display: none;
  width: 84px;
  height: 100%;
  position: absolute;
  right: 0;
  top: 0;
  border-radius: 0 12px 12px 0;
  background: linear-gradient(270deg, #fff 50%, #f2f2f500);
  z-index: 2;
}

.action-item-delete {
  position: absolute;
  right: 8px;
}

.active-item {
  background: #d7f6ff;
  box-shadow: 0 2px 6px #0000001a;
}

.chat-history-message {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-container {
  display: flex;
}


.concersation-container {
  width: 100%;
  height: 100%;
  background: #fff;
  border-radius: 10px;
}

.message-container {
  height: calc(100% - 150px);
  overflow-y: auto;
  box-sizing: border-box;
  padding: 10px;
  padding-bottom: 20px;
}

.submit-container {
  height: 150px;
  padding: 5px;
  display: flex;
  flex-direction: column;
  position: relative;
}

.recommend-container {
  position: absolute;
  top: -25px;
  display: flex;
  z-index: 1;
}

.prefix-desc {
  color: #999AAA;
}

.tip-desc {
  display: flex;
}

.tip-item {
  cursor: pointer;
  margin-right: 10px;
  background: #6fd8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
  box-shadow: 0px 2px 4px 0px rgb(0 0 0 / 15%);
  color: #fff;
  padding: 0 10px;
  border-radius: 10px;
}

.text-container {
  flex: 1;
}

.btn-container {
  display: flex;
  justify-content: space-between;
}

.ai-message-container {
  display: flex;
  align-items: start;
  box-sizing: border-box;
  width: 100%;
  margin-bottom: 10px;
}

.human_message-container {
  display: flex;
  align-items: start;
  box-sizing: border-box;
  justify-content: end;
  width: 100%;
  margin-bottom: 10px;
}

.ai-logo {
  align-items: end;
  height: 50px;
  margin-right: 10px;
  border-radius: 50%;
  box-shadow: 0px 2px 4px 0px rgb(0 0 0 / 15%);
}

.ai-logo img {
  height: 50px;
  border-radius: 50%;
}

.ai-message {
  position: relative;
  display: inline-block;
  margin: 0 0 0 15px;
  padding: 20px 10px;
  min-width: 120px;
  max-width: 90%;
  color: #555;
  font-size: 16px;
  background: #e0f2ff;
  border-radius: 5px;
}

.ai-message:before {
  content: "";
  position: absolute;
  top: 30px;
  left: -29px;
  margin-top: -15px;
  border: 15px solid transparent;
  border-right: 15px solid #e0f2ff;
}

.human-logo {
  width: 50px;
  height: 50px;
  margin-left: 10px;
  border-radius: 50%;
  box-shadow: 0px 2px 4px 0px rgb(0 0 0 / 15%);

  img {
    width: 100%;
    border-radius: 50%;
  }
}

.human-message {
  position: relative;
  display: inline-block;
  margin: 0 15px 0 0;
  padding: 20px 10px;
  min-width: 120px;
  max-width: 90%;
  float: right;
  clear: both;
  color: #555;
  font-size: 16px;
  background: #e0f2ff;
  border-radius: 5px;
  white-space:pre-wrap;
  word-break: break-word;
}

.human-message:before {
  content: "";
  position: absolute;
  top: 30px;
  left: 100%;
  margin-top: -15px;
  border: 15px solid transparent;
  border-left: 15px solid #e0f2ff;
}

.conversation {
  display: flex;
  justify-content: space-between;
}

.conversation-title {
  overflow: hidden;
  /* 隐藏超出部分 */
  text-overflow: ellipsis;
  /* 使用省略号表示被省略的内容 */
  white-space: nowrap;
  flex: 1;
  cursor: pointer;
}

.conversation-btn {
  width: 20px;
}

.conversation-list {
  width: 100%;
  height: calc(100% - 50px);
  overflow-y: scroll;
}

.conversation-add {
  width: 100%;
}

.controller-container{
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
}
.controller-item{
  display: flex;
  height: 50px;
  align-items: center;
  width: 100%;
  justify-content: space-between;
  .item{
    width: 90%;
  }
}
.controller-label{
  width: 100px;
  box-sizing: border-box;
  padding-left: 5px;
  text-align: right;
}
.controller-compoment{
  flex: 1;
  display: flex;
  justify-content: end;
  box-sizing: border-box;
  padding-right: 30px;
}

/* 整个滚动条 */
::-webkit-scrollbar {
  width: 5px;
  /* 滚动条的宽度 */
  height: 10px;
  /* 滚动条的高度，对水平滚动条有效 */
  position: absolute;
}

/* 滚动条轨道 */
::-webkit-scrollbar-track {
  border-radius: 10px;
}

/* 滚动条滑块 */
::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-color: #c1c1c1;
  /* 滑块的背景颜色 */
  border: 3px solid #e1e1e1;
  /* 滑块的边框和轨道相同的颜色，可以制造“边距”的效果 */
}

::-webkit-scrollbar-thumb:hover {
  background-color: #d4d4d4;
  /* 滑块的悬停颜色 */
}

::-webkit-scrollbar-thumb:active {
  background-color: #d3d3d3;
  /* 滑块的激活颜色 */
}

::-webkit-scrollbar-button {
  display: none;
}

.message-container-index {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-content: center;
  align-items: center;
}

.index-logo {
  width: 400px;

  img {
    width: 100%;
  }
}

.title {
  font-size: 14px;
}

.question-list-container {
  width: 1036px;

  .questuon-list-head {
    display: flex;
    justify-content: space-between;
    margin: 30px 0 12px 0;

    .left {
      color: #999AAA;
    }
  }

  .question-item {
    background: #0000000d;
    padding: 12px 8px;
    border-radius: 12px;
    cursor: pointer;
  }

  .title-line {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .col {
    margin-bottom: 20px;
  }
}
.recommend{
  margin-top: 10px;
  font-size: 15px;
  border-top: #e1e1e1 1px solid;
}
.recommend-file{
  border-bottom: #d7f6ff 1px solid;
}
.docItem{
  cursor: pointer;
  &:hover{
    color: rgb(255, 110, 37);
  }
}
</style>