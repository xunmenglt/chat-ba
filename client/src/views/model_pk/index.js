import PK from './components/pk' 
import ChatBox from './components/chatbox'
import { EventBus } from '@/utils/eventBus'
import { getModelList } from '@/utils/api/model.js'
import { generateUUID } from '@/utils/utils'
import { PkReport } from '@/utils/api/pk'
export default {
    name:"model_pk",
    components:{PK,ChatBox},
    data() {
        return {
            // 输入的问题
            query:"",
            add_dialogVisible:false,
            temperature:95,
            max_tokens:50,
            top_p:90,
            // 报告数据
            reportDate:[],
            showReport:false,
            modelItemTemp:{
                id:"",
                model_name: "",
                history_len: 3,
                stream: true,
                temperature: 0.95,
                max_tokens: 512,
                top_p:0.9, 
            },
            modelBoxList:[],
            modelList:[]
        }
    },
    created() {
        // 删除足
        if(document.getElementById('foot')){
            document.getElementById('foot').remove()
        }
        this.initModelList()
    },
    methods: {
        handlerAddModel(){
            if(this.modelList.length>0){
                for (let i=0; i<this.modelList.length;i++){
                    let flag=false
                    for (let j=0;j<this.modelBoxList.length;j++){
                        if(this.modelList[i]===this.modelBoxList[j].model_name){
                            flag=true
                            break
                        }
                    }
                    if(!flag && this.modelBoxList.length>0){
                        this.modelItemTemp.model_name=this.modelList[i]
                        break
                    }else{
                        this.modelItemTemp.model_name=this.modelList[0]
                    }
                }
            }
            this.add_dialogVisible=true
        },
        addModel(){
            let id=generateUUID()
            this.modelItemTemp.id=id
            this.modelBoxList=[...this.modelBoxList,this.modelItemTemp]
            this.refashModelItemTemp()
            this.add_dialogVisible=false
        },
        handleDeleteModelItem(mode_id){
            this.modelBoxList=this.modelBoxList.filter((e)=>e.id!==mode_id)
        },
        handleInputBlur(){
            document.getElementById('textarea-with-actions-container').className=""
        },
        handleInputFocus(){
            document.getElementById('textarea-with-actions-container').className="input-focus"
        },
        onKeyUpSend(event) {
            // 检查是否同时按下了Ctrl和Enter键
            if (event.ctrlKey && event.keyCode === 13) {
              // 触发发送文本的函数
              this.handleSubmitForm()
            }
        },
        handleSubmitForm(){
            if(this.query){
                let input=this.query
                EventBus.$emit('modelPkSubmitEvent',input)
                this.query=''            
            }
        },
        refashModelItemTemp(){
            this.modelItemTemp={
                id:"",
                model_name: "",
                history_len: 3,
                stream: true,
                temperature: 0.7,
                max_tokens: 512,
                top_p:0.9, 
            }
        },
        initModelList(){
            getModelList().then(res => {
              this.modelList = res.data
              if(this.modelList.length>0){
                this.modelItemTemp.model_name=this.modelList[0]
              }
            }).catch(e => {
            })
        },
        // 格式化
        formatTemperature(val) {
            let value = val / 100
            this.modelItemTemp.temperature = value
            return value
        },
        formatTop_p(val) {
            let value = val / 100
            this.modelItemTemp.top_p = value
            return value
        },
        formatMax_tokens(val) {
            let value = Math.floor(val * (2048 / 100))
            this.modelItemTemp.max_tokens = value
            return value
        },
        createReport(){
            if(this.reportDate && this.reportDate.length>0){
                this.showReport=true
            }else{
                this.flashReport()
            }
        },
        flashReport(){
            let data=[]
            this.modelBoxList.forEach((model)=>{
                let messages=[]
                if(this.$refs[`model-${model.id}`]){
                    messages=this.$refs[`model-${model.id}`][0].messages
                }
                let item={...model,messages:messages}
                data.push(item)
            })
            this.$modal.loading("PK报告生成中...")
            PkReport(data).then(res=>{
                this.reportDate=res.data
                this.showReport=true
            }).catch(e=>{
                alert('报告生成异常')
                this.showReport=false
            }).finally(()=>{
                this.$modal.closeLoading()
            })
        }
    },
    computed:{
        showCreateReport(){
            let flag=false
            if(this.modelBoxList && this.modelBoxList.length>0){
                this.modelBoxList.forEach(model_box=>{
                    let model=model_box
                    if(this.$refs[`model-${model.id}`]){
                        let messages=this.$refs[`model-${model.id}`][0].messages
                        if(messages && messages.length>0){
                            flag=true
                        }else{
                            flag=false
                        }
                    }
                })
            }
            return flag
        }
    }
}