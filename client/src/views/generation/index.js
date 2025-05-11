import {uploadKnowledgeFileApi} from '@/utils/api/generation'
import QABox from './qabox.vue'
export default{
    name:"generation",
    components:{QABox},
    data() {
        return {
            currentFileInfo:{},
            // 文件上传弹出框
            fileUploadWinShow:false,
            uplodFileList:[],
            upload_id:"",
            qa_box_ids:[]
        }
    },
    created() {
        this.addUseCase()
    },  
    methods: {
        createRandQaBoxID(){
            let id=String(new Date().getTime())
            return id
        },
        addUseCase(){
            this.qa_box_ids.push(this.createRandQaBoxID())
        },
        deleteUseCase(qa_box_id){
            if (this.qa_box_ids && this.qa_box_ids.length>0){
                let tmp_list=[]
                this.qa_box_ids.forEach(element => {
                    if (element!==qa_box_id){
                        tmp_list.push(element)
                    }
                });
                this.qa_box_ids=tmp_list
            }
        },
        cancleUploadFile(){
            this.uplodFileList=[]
            this.currentFileInfo={}
            this.fileUploadWinShow=false
        },
        doUploadFile(){
            if (this.currentFileInfo){
                this.$modal.loading("正在上传文件")
                uploadKnowledgeFileApi({
                    files:this.uplodFileList.map(element => element.raw)
                }).then((res=>{
                    console.log(res)
                    this.upload_id=res.data.upload_id
                })).catch(()=>{
                    this.$modal.msgError("文件上传失败，请重试")
                }).finally(()=>{
                    this.fileUploadWinShow=false
                    this.$modal.closeLoading()
                })
                this.fileUploadWinShow=false
            }
            this.fileUploadWinShow=false

        },
        uploadFilehandleChange(file,fileList){
            if (fileList && fileList.length>0){
                let len=fileList.length
                let file=fileList[len-1]
                if (file && file.name.indexOf('.pdf')==-1){
                    this.uplodFileList=[]
                    this.currentFileInfo={}
                    this.$modal.msgWarning("只支持PDF文件，请重新上传")
                    return
                }
                file.file_id=new Date().getTime() // # 以时间戳作为唯一标识
                this.currentFileInfo=file
                this.uplodFileList=[this.currentFileInfo]
            }
        },
    },
}