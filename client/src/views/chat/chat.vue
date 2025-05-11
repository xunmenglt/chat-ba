<template>
  <div class="content-container">

    <el-drawer title="设置" :visible.sync="showSetting" :direction="'ltr'" size="30%">
      <div class="add-container">
        <v-btn class="ma-2 add-btn" color="info" @click="createConversation"><v-icon dark>
            mdi-plus
          </v-icon>
          新建对话</v-btn>
      </div>
      <div class="conversation-list-container">
        <div :class="['win-item', win.id == require_data.conversation_id ? 'active-item' : '']" v-for="win in winList"
          :key="win.id" @click="changeWin(win.id)">
          <div class="win-item-wrap">
            <div class="win-item-title">
              <span style="margin-right: 4px;">
                <v-icon>
                  mdi-message-processing-outline
                </v-icon>
              </span>
              <span class="chat-history-message">
                {{ win.name }}
              </span>
            </div>
          </div>

          <div class="his-action">
            <div class="action-item action-item-delete" @click.stop="toDeleteWin(win.id)">
              <v-icon style="  color: red;">
                mdi-delete-forever
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
              <el-select v-model="require_data.prompt_name" clearable placeholder="请选择">
                <el-option v-for="item in promptList" :key="item" :label="item" :value="item">
                </el-option>
              </el-select>
            </div>
            <el-popover placement="bottom" title="模板内容" trigger="click" width="400">
              <div style="white-space:pre-wrap;">{{ promptInfo }}</div>
              <el-button slot="reference" type="text" @click="toGetPromptInfo"><i
                  class="el-icon-view"></i>查看模板</el-button>
            </el-popover>
          </div>
          <div class="controller-item">
            <div class="controller-label">
              历史对话数:
            </div>
            <div class="controller-compoment">
              <el-input-number class="item" v-model="require_data.history_len" :min="0" :max="5"></el-input-number>
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
            <div class="human-message message">{{ message['query'] }}</div>
            <div class="human-logo">
              <img :src="PersonImage">
            </div>
          </div>
          <div v-if="message['response'] || !canSend" class="ai-message-container">
            <div class="ai-logo">
              <img :src="RobotImage">
            </div>
            <div class="ai-message message">
              <messageVue :value="message['response']" />
            </div>
            <v-progress-circular v-if="message['is_sending']" indeterminate color="primary"
              :size="20"></v-progress-circular>
          </div>
        </div>
      </div>
      <div class="submit-container">
        <div class="text-container">
          <el-input :disabled="!canSend" type="textarea" maxlength="8192" show-word-limit resize="none" :rows="4"
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

    <!-- 新建对话窗 -->
    <el-dialog title="新建对话窗" :visible.sync="add_dialogVisible" width="30%" :close-on-click-modal="false">
      <div class="controller-compoment">
        <el-input class="item" v-model="newWin.name" placeholder="请输入对话名称"></el-input>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="add_dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="doCreateConversation">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import '@/assets/js/china.js'
import RobotImage from '@/assets/icons/robot.png'
import PersonImage from '@/assets/icons/person.png'
import messageVue from '@/components/message/message.vue'
import { getWinList, createWin, deleteWin, getHistoryMessageList } from '@/utils/api/win.js'
import { getModelList } from '@/utils/api/model.js'
import { getPromptList, getPromptInfo } from '@/utils/api/prompt.js'
import { showTextMessage } from '@/plugins/toastification'
import { TYPE } from 'vue-toastification'
import { DialogueChat } from '@/utils/api/chat'
import Vue from 'vue';
import { Skeleton } from 'element-ui';

export default {
  components: { messageVue },
  data() {
    return {
      temperature: 95,
      max_tokens: 6.25,
      top_p: 90,
      require_data: {
        query: "",
        conversation_id: "",
        model_name: "",
        history_len: 3,
        stream: true,
        temperature: 0.7,
        max_tokens: 512,
        top_p: 0.9,
        prompt_name: "default"
      },

      add_dialogVisible: false,
      new_conversation_title: "",

      PersonImage: PersonImage,
      RobotImage: RobotImage,
      modelList: [],
      promptList: [],
      promptInfo: "",
      activateId: "",
      showSetting: false,
      showHightSetting: false,
      canSend: true,
      winList: [],
      currentReplayMessage: {},
      docs: [],
      messageList: [
      ],
      newWin: {
        "name": "普通对话",
        "type": "dialogue"
      }
    }
  },
  mounted() {
    window.addEventListener("keydown", this.quickSend, false);
    this.parseAllEcharts()
  },
  destroyed() {
    window.removeEventListener("keydown", this.quickSend);
  },
  async created() {

    await this.initWinList()
    if (this.winList && this.winList.length > 0) {
        this.changeWin(this.winList[0].id)
    }
    await this.initModelList()
    await this.initPromptList()
    this.parseAllEcharts()
  },

  methods: {
    createSkeletonComponent(chartdiv){
      const SkeletonComponent  = Vue.extend({
                  components: { ElSkeleton: Skeleton }, // 引入 Element UI 的 input 组件
                  render(h) {
                    return h(
                      'el-skeleton',
                      {
                        props: { rows: 1, animated: true }
                      }
                    );
                  }
                });
       // 2. 创建组件实例
       const skeletonInstance = new SkeletonComponent();
       skeletonInstance.$mount(chartdiv)
    },
    parseAllEcharts() {
      let aimessageboxs = document.getElementsByClassName("ai-message")
      setTimeout(() => {
        for (let i = 0; i < aimessageboxs.length; i++) {
          let echartCodes = aimessageboxs[i].getElementsByClassName('lang-echarts')

          // 获取每一个codebox
          if (echartCodes && echartCodes.length > 0) {
            let echartCodesLength = echartCodes.length
            
            for (let eci = 0; eci < echartCodesLength; eci++) {
              const echartCode = echartCodes[eci]
              if (!echartCode){
                continue
              }
              const chartdiv = document.createElement('div')
              chartdiv.id = `${new Date().getTime()}`
              echartCode.replaceWith(chartdiv)
              try{
                const jsonDate = eval(`(${echartCode.innerText})`)
                const option = jsonDate.option
                chartdiv.style.width='600px'
                chartdiv.style.height='300px'
                chartdiv.style.width=chartdiv.parentNode.offsetWidth
                let chart = echarts.init(chartdiv)
                chart.setOption(option)
                window.addEventListener("resize", () => {
                  chart.resize();
                });    
              }catch(err){
                this.createSkeletonComponent(chartdiv)
              }
            }
          }
        }

      }, 200)

    },
    async initWinList() {
      const res = await getWinList()
      if (res &&res.code==200){
        this.winList = res.data.reverse()
      }else{
        showTextMessage(TYPE.ERROR, "获取对话窗异常")
      }
    },
    async initModelList() {
      const res=await getModelList()
      if (res &&res.code==200){
        this.modelList = res.data
        if (this.modelList.length > 0) {
          this.require_data.model_name = this.modelList[0]
        }
      }else{
        showTextMessage(TYPE.ERROR, "获取模型列表异常")
      }
      
    },
    async initPromptList() {
      const res = await getPromptList({ type: "dialogue" })
      if (res &&res.code==200){
        this.promptList = res.data
        if (this.promptList.length > 0) {
          this.require_data.prompt_name = this.promptList[0]
        }
      }else{
        showTextMessage(TYPE.ERROR, "获取模板列表异常")
      }
    },
    initHistoryMessageList() {
      getHistoryMessageList(this.require_data.conversation_id).then(res => {
        this.messageList = res.data
        this.flashScroll()
      }).catch(e => {
        showTextMessage(TYPE.ERROR, `获取历史信息异常`)
      })
    },
    toGetPromptInfo() {
      getPromptInfo({ type: "dialogue", prompt_name: this.require_data.prompt_name }).then(res => {
        if (res.data) {
          this.promptInfo = res.data
        }
      }).catch(e => {
        showTextMessage(TYPE.ERROR, `获取模板【${this.require_data.prompt_name}】信息异常`)
      })
    },
    toDeleteWin(winId) {
      this.$modal.confirm('是否确认删除对话框"').then(function () {
        return deleteWin(winId)
      }).then(() => {
        this.initWinList().then(() => {
          if (this.winList && this.winList.length > 0) {
            this.changeWin(this.winList[0].id)
          }
        })
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {
      })
    },

    // 新建对话窗口
    createConversation() {
      this.add_dialogVisible = true
    },
    doCreateConversation() {
      createWin(this.newWin).then(res => {
        this.$modal.msgSuccess("创建成功");
        this.initWinList().then((res) => {
          if (this.winList && this.winList.length > 0) {
            this.changeWin(this.winList[0].id)
          }
        })
      }).catch(e => {
        this.$modal.msgError("创建失败");
      }).finally(_ => {
        this.add_dialogVisible = false
      })

    },
    changeWin(winId) {
      this.require_data.conversation_id = winId
      this.initHistoryMessageList()
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
    quickSend(e) {
      let that = this
      if (e.ctrlKey && e.keyCode == 13) {
        that.handlerSendMessage()
      }
    },
    handlerSendMessage() {
      if (!this.require_data.conversation_id) {
        // 创建新的对话框
        this.$modal.msgWarning("请选择对话窗")
        return
      }
      this.doSendMessage()
    },
    doSendMessage() {
      if (this.canSend && this.require_data.query) {
        this.canSend = false
        let newMessage = {
          query: this.require_data.query + '',
          response: '',
          is_sending: true,
        }
        this.messageList.push(newMessage)
        this.currentReplayMessage = newMessage
        this.flashScroll()
        DialogueChat(this.require_data,
          this.readCallback,
          this.endCallback
        )
      }
    },
    readCallback(isfirst, chunkValue) {
      let data_object = null
      try {
        data_object = JSON.parse(chunkValue.substring("data:".length, chunkValue.length).trim())
      } catch (error) {
        return
      }
      if (data_object["answer"]) {
        let text = data_object["answer"]
        this.currentReplayMessage.response += text
      }
      if (data_object["docs"] != undefined) {
        this.docs = data_object["docs"]
      }
      this.flashScroll()
    },
    endCallback() {
      this.currentReplayMessage.is_sending = false
      this.canSend = true
      this.require_data.query = ""
      this.parseAllEcharts()
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
      let value = Math.floor(val * (8192 / 100))
      this.require_data.max_tokens = value
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
  height: 100%;
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
  z-index: 2001;
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

.message {
  margin-bottom: 8px;
  border: 1px solid #e7e7e9;
  color: #2e3238;
  padding: 12px;
  border-radius: 10px;
}

.ai-logo {
  align-items: end;
  height: 35px;
  width: 35px;
  margin-right: 10px;
  border-radius: 50%;
  box-shadow: 0px 2px 4px 0px rgb(0 0 0 / 15%);
}

.ai-logo img {
  height: 35px;
  border-radius: 50%;
}



.human-logo {
  width: 35px;
  height: 35px;
  margin-left: 10px;
  border-radius: 50%;
  box-shadow: 0px 2px 4px 0px rgb(0 0 0 / 15%);

  img {
    width: 35px;
    border-radius: 50%;
  }
}

.human-message {
  --uikit-message-box-primary-background-color: linear-gradient(269deg, #a171ff -3.63%, #5d66ff 100.38%);
  --uikit-message-box-whiteness-background-color: #fff;
  --uikit-message-box-box-shadow-color: rgba(10, 17, 61, .06);
  --uikit-chat-input-primary-color: #f5f6f8;
  background: var(--uikit-message-box-primary-background-color, #4d53e8);
  border: 1px solid #e7e7e9;
  color: #fff;
  padding: 12px;
  box-shadow: 0 32px 50px -12px var(--uikit-message-box-box-shadow-color, transparent);

  /deep/ .markdown-body {
    color: #fff !important;
  }
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

.controller-container {
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
}

.controller-item {
  display: flex;
  height: 50px;
  align-items: center;
  width: 100%;
  justify-content: space-between;

  .item {
    width: 90%;
  }
}

.controller-label {
  width: 100px;
  box-sizing: border-box;
  padding-left: 5px;
  text-align: right;
}

.controller-compoment {
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

/deep/ .v-show-content {
  padding: 0 !important;
  background-color: #ffffff00 !important;
  word-break: break-word;

  p {
    margin: 0 !important;
  }
}

/deep/ .markdown-body {
  color: #2e3238;
  font-size: 14px;
  line-height: 1.5;
}

/deep/ .v-note-wrapper {
  background: none !important;
}

/deep/ code {
  white-space: pre-wrap;
}
/deep/ pre{
  position: relative !important;
  width: 100% !important;
}
</style>
