<template>
  <div class="chat-box-container">
    <div class="head">
      <div class="right">
        <div class="chat-title">
          {{ model.model_name }}
        </div>
      </div>
      <div class="left">
        <div class="opt-item">
          <v-btn
              class="ma-2"
              x-small
              outlined
              color="red"
              @click="deleteModelItem"
            >
            <i class="icon el-icon-error"></i> 删除
          </v-btn>
        </div>
      </div>
    </div>
    <div class="message-container" v-if="messages&&messages.length>0" :id="`message-container-${model.id}`">
      <div class="message-item" v-for="(item,index) in messages" :key="index">
        <div class="avatar-container">
          <span class="avatar">
            <img v-if="item.role===ASSISTANT" src="../../images/GPT4.png">
            <img v-else src="../../images/user.png">
          </span>
        </div>
        <div class="content-message">
          <div class="role-name">
            <div class="right">
              <span v-if="item.role===ASSISTANT">Assistant</span>
              <span v-else> YOU </span>
            </div>
            <div class="left">
              <div class="startTime">{{formatStartTime(item)}}</div>
            </div>
          </div>
          <div :class="['message',item.role===ASSISTANT?'':'user-message']">
            <messageVue :value="item['content']" />
          </div>
          <div v-if="item && item.startTime && item.role===ASSISTANT" class="totalTime">
            <i v-if="item.endTime" class="icon el-icon-check"></i>
            <i v-else class="icon el-icon-loading"></i>
            {{formatDate(item)}}s
          </div>
        </div>
      </div>
      <div v-if="(completion && completion.content)|| generating" class="message-item">
        <div class="avatar-container">
          <span class="avatar">
            <img src="../../images/GPT4.png">
          </span>
        </div>
        <div class="content-message">
          <div class="role-name">
            <div class="right">
              <span>Assistant</span>
            </div>
          </div>
          <div :class="['message', completion.role === ASSISTANT ? '' : 'user-message']">
            <messageVue :value="completion['content']" />
          </div>
          <!-- <div v-if="(completion && completion.startTime && completion.role===ASSISTANT) || generating" class="totalTime">
            <i v-if="!generating" class="icon el-icon-check"></i>
            <i v-else class="icon el-icon-loading"></i>
            {{formatDate(completion)}}s
          </div> -->
          <div class="totalTime">
            <i v-if="!generating" class="icon el-icon-check"></i>
            <i v-else class="icon el-icon-loading"></i>
            {{formatDate(completion)}}s
          </div>
        </div>
      </div>
    </div>
    <div class="chat-bg" v-else>
      <img :src="require(`../../images/chat_${Math.floor(Math.random()*10)}.png`)"/>
    </div>
    <div class="mask" v-if="generating">
      <div class="stop-btn-container">
        <el-button round @click="stopGenerating">
          <i class="iconfont icon-stopcircle" style="margin-right:5px;"></i>停止响应
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import messageVue from '@/components/message/message.vue'
import { EventBus } from '@/utils/eventBus'
import {PKChat} from '@/utils/api/pk'
export default {
  components:{messageVue},
  props:{
    model:{
      type:Object,
      default:{}
    }
  },
  data() {
    return {
      ASSISTANT:"assistant",
      USER:"user",
      SYSTEM:"system",
      generating:false,
      controller:null,
      messages:[
      ],
      completion:{
        role: "assistant",
        content: ""
      }
    }
  },
  created(){
    EventBus.$on('modelPkSubmitEvent',this.handlerSubmit)
  },
  beforeDestroy(){
    // EventBus.$off('modelPkSubmitEvent');
  },
  methods:{
    formatDate(item){
      let totalTime=0
      if(item){
        debugger
        let currentTime=new Date().getTime()
        if(item.endTime){
          currentTime=item.endTime
        }
        let startTime=new Date().getTime()
        if(item.startTime){
          startTime=item.startTime
        }
        totalTime=(currentTime-startTime)/1000
      }
      return Math.round(totalTime * 10) / 10
    },
    formatStartTime(item){
      let currentTime=new Date()
      if(item && item.startTime){
        currentTime=new Date(item.startTime)
      }
      let hours = String(currentTime.getHours()).padStart(2, '0');
      let minutes = String(currentTime.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`
    },
    deleteModelItem(){
      if(this.model){
        this.$emit("handleDeleteModelItem",this.model.id)
      }
    },
    scrollToBottom(){
      if(document.getElementById(`message-container-${this.model.id}`)){
        const conversationContainer = document.getElementById(`message-container-${this.model.id}`);
        conversationContainer.scroll({
            top: conversationContainer.scrollHeight,
            behavior: 'smooth'
        })
      }
    },
    handlerSubmit(query){
      if(query && !this.generating){
        let startTime=new Date().getTime()
        this.messages=[...this.messages,{"role":'user',"content":query,"startTime":startTime}]
        this.generating=true
        this.scrollToBottom()
        this.completion.startTime=startTime
        PKChat({...this.model,messages:this.messages},
          this.readCallback,
          this.endCallback,
          this.startCalback
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
        this.completion.content+=text
      }
      if (data_object["startTime"] != undefined) {
        this.completion.startTime=data_object["startTime"]
      }
      if (data_object["endTime"] != undefined) {
        this.completion.endTime=data_object["endTime"]
      }
      if (data_object["usage"] != undefined) {
        this.completion.usage=data_object["usage"]
      }
      setTimeout(()=>{
        this.scrollToBottom()
      },200)
    },
    endCallback(){
      if(this.completion && this.completion.content){
        this.messages=[...this.messages,this.completion]
      }
      this.completion={
        role:'assistant',
        content:''
      }
      this.generating=false
      setTimeout(()=>{
        this.scrollToBottom()
      },200)
    },
    startCalback(controller){
      if(controller){
        this.controller=controller
      }
    },
    stopGenerating(){
      debugger
      if(this.controller && this.generating){
        const { signal } = this.controller
        if (signal && !signal.aborted){
          this.controller.abort()
        }
      }
    }
  }
}
</script>

<style lang="less" scoped>
.chat-box-container{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}
.stop-btn-container{
  /deep/ .el-button{
    color: #4d53e8;
  }
}
.mask{
  width: 100%;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  bottom: 0;
}
.head{
  height: 30px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
  .chat-title{
    font-size: 16px;
    font-weight: 700;
  }
  .right{
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .left{
    display: none;
    align-items: center;
    justify-content: center;
  }
}
.head:hover{
  .left{
    display: flex;
  }
}
.opt-item{
  margin-left: 5px;
  cursor: pointer;
}
.message-container{
  overflow-y: auto;
  box-sizing: border-box;
}

.message-item{
  padding-top: 10px;
  display: flex;
  .avatar{
    height: 32px;
    margin-right: 12px;
    width: 32px;
    img{
      height: 32px;
      width: 32px;
      border-radius: 50%;
    }
  }
  .role-name{
    color: #383743;
    font-size: 14px;
    font-weight: 900;
    display: flex;
    justify-content: space-between;
  }
  .startTime{
    display: none;    
  }
  .totalTime{
    font-weight: normal;
    font-size: 14px;
    color: #b0b0b0;
  }
}
.message-item:hover{

  .startTime{
    display: block;
    font-weight: normal;
    font-size: 14px;
    color: #b0b0b0;
  }
}
.message{
  margin-bottom: 8px; 
  border: 1px solid #e7e7e9;
  color: #2e3238;
  padding: 12px;
  border-radius: 10px;
}
.user-message{
    --uikit-message-box-primary-background-color: linear-gradient(269deg,#a171ff -3.63%,#5d66ff 100.38%);
    --uikit-message-box-whiteness-background-color: #fff;
    --uikit-message-box-box-shadow-color: rgba(10,17,61,.06);
    --uikit-chat-input-primary-color: #f5f6f8;
    background: var(--uikit-message-box-primary-background-color,#4d53e8);
    border: 1px solid #e7e7e9;
    color: #fff;
    padding: 12px;
    box-shadow: 0 32px 50px -12px var(--uikit-message-box-box-shadow-color,transparent);
    /deep/ .markdown-body{
      color: #fff !important;
    }
}
.chat-bg{
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  img{
    height: 220px;
  }
}
/deep/ code{
  white-space: pre-wrap;
}
/deep/ .v-show-content{
  padding: 0 !important;
  background-color: #ffffff00 !important;
  word-break: break-word;
  p{
      margin: 0 !important;
  }
}
/deep/ .markdown-body{
  color: #2e3238;
  font-size: 14px;
  line-height: 1.5;
}
/deep/ .v-note-wrapper{
  background: none !important;
}
::-webkit-scrollbar {
  width: 0px;
}
</style>