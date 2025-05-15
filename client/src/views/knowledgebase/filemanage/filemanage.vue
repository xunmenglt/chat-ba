<template>
    <div class="knowledgebase-container">
        <div class="top-slider d-flex">
            <div class="title">
                <i class="back-icon mdi mdi-arrow-left" @click="backKBS"></i>
                <div class="kbinfo">
                    <div class="kb_name">知识库{{kb_info.kb_name}}</div>
                    <div class="kb_info">{{kb_info.kb_info}}</div>
                </div>
            </div>
            <div class="opt-container">
                <el-button @click="uploaddialog=true" type="primary">
                    <i class="el-icon-upload"></i> 上传知识
                </el-button>
            </div>
        </div>
        <el-divider></el-divider>
        <div class="file-list-container d-flex flex-wrap justify-space-start">
            <el-table :data="data_list" :stripe="true" style="width: 100%;" height="calc(100vh - 250px)">
                <el-table-column v-for="header in file_table_headers" :key="header.value" :label="header.text" :prop="header.value" :sortable="header.sortable">
                    <template v-if="header.value === 'actions'" v-slot="scope">
                        <el-button @click="delete_item=scope.row;deletefiledialog=true" type="text" icon="el-icon-delete"></el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 上传知识库 -->
        <el-dialog :visible.sync="uploaddialog" title="上传知识文件" width="600px">
            <el-form size="mini">
                <el-form-item label="知识文件">
                    <el-upload 
                        class="upload-demo" 
                        drag 
                        multiple 
                        action="#"
                        :on-change="handleFileChange"
                        :on-remove="handleFileRemove"
                        :limit="1000"
                        :auto-upload="false"
                        accept=".pdf,.doc,.docx,.jsonl,.txt"
                    >
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                </el-form-item>
                <el-form-item label="是否覆盖">
                    <el-select v-model="override">
                        <el-option label="是" :value="true"></el-option>
                        <el-option label="否" :value="false"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="是否向量化">
                    <el-select v-model="is_vector_store" required>
                        <el-option label="是" :value="true"></el-option>
                        <el-option label="否" :value="false"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="文档切分长度">
                        <el-slider v-model="chunk_size" :max="1024" :min="100" :step="1"></el-slider>
                </el-form-item>
                <el-form-item label="相邻文档重合长度">
                    <el-slider v-model="chunk_overlap" :max="500" :min="1" :step="1"></el-slider>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="uploaddialog = false">取消</el-button>
                <el-button type="primary" @click="doUploadFile">确认</el-button>
            </div>
        </el-dialog>

        <!-- 删除文件弹窗 -->
        <el-dialog :visible.sync="deletefiledialog" title="确认删除" width="400px">
            <div>您是否要删除 <span style="color:#616161;margin-left:5px">{{delete_item.file_name}}</span>?</div>
            <div>删除操作将导致知识文件被删除以及向量库中对应数据将被删除，请谨慎操作!</div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="deletefiledialog = false">不同意</el-button>
                <el-button type="danger" @click="toDeletefile">同意</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { 
    getKnowledgeFileListApi,
    deleteKnowledgeFileApi,
    uploadKnowledgeFileApi
} from '@/utils/api/knowledgedoc';

export default {
    data() {
        return {
            file_table_headers:[
                { text: '文件ID', value: 'id' }, 
                { text: '文件名称', value: 'file_name' },
                { text: '扩展类型', value: 'file_ext' },
                { text: '所属知识库', value: 'kb_name' },
                { text: '文档加载器', value: 'document_loader_name' },
                { text: '文本分割器', value: 'text_splitter_name' },
                { text: '文件大小', value: 'file_size' },
                { text: '文档切分数量', value: 'docs_count' },
                { text: '创建时间', value: 'create_time' },
                { text: 'Actions', value: 'actions', sortable: false },
            ],
            kb_info: {},
            data_list: [],
            uploaddialog: false,
            deletefiledialog: false,
            delete_item: {},
            upload_fileList:[],
            chunk_size: 450,
            chunk_overlap: 20,
            is_vector_store: true,
            override: true
        }
    },
    created(){
        this.kb_info = this.$route.query;
    },
    mounted(){
        this.flashDataList();
    },
    methods: {
        async flashDataList(){
            if (this.kb_info.kb_name){
                let response = await getKnowledgeFileListApi({"factory_name": this.kb_info.kb_name});
                if (response && response.code && response.code == 200){
                    this.data_list = response.data;
                } else {
                    this.$modal.msgError( `服务异常：${response.msg}`)
                }
            }
        },
        backKBS(){
            this.$router.push("/dashboard/knowledgebase");
        },
        async toDeletefile(){
            if (this.delete_item && this.delete_item.kb_name && this.delete_item.file_name){
                let response = await deleteKnowledgeFileApi({
                    "factory_name": this.delete_item.kb_name,
                    "file_name": this.delete_item.file_name
                });
                if (response && response.code && response.code == 200){
                    this.$modal.msgSuccess( response.msg)
                    this.flashDataList().then(
                        this.deletefiledialog = false
                    );
                } else if (response && response.code){
                    this.$modal.msgError( response.msg)

                    this.deletefiledialog = false;
                }
            }
        },
        async doUploadFile(){
            this.$modal.loading("正在上传文件");
            let files=[]
            if (this.upload_fileList && this.upload_fileList.length>0){
                files=this.upload_fileList.map((f)=>f.raw)
            }
            if (!files || files.length<=0){
                this.$modal.msgWarning("文件不能为空")
                this.$modal.closeLoading();
                return
            }
            let item = {
                files: files,
                chunk_size: this.chunk_size,
                chunk_overlap: this.chunk_overlap,
                is_vector_store: this.is_vector_store,
                override: this.override,
                factory_name: this.kb_info.kb_name
            };
            if (this.kb_info && this.kb_info.kb_name){
                let response = await uploadKnowledgeFileApi(item);
                if (response && response.code && response.code == 200){
                    this.$modal.msgSuccess(response.msg)
                    this.flashDataList().then(
                        this.uploaddialog = false
                    );
                } else if (response && response.code){
                    this.$modal.msgError(response.msg)
                    this.uploaddialog = false;
                }
            }
            this.$modal.closeLoading();
        },
        handleFileChange(e){
            this.upload_fileList.push(e)
        },
        handleFileRemove(e){
            if(e && this.upload_fileList){
                this.upload_fileList=this.upload_fileList.filter((f)=>f!=e)
            }
        }
    }
}
</script>

<style lang="less" scoped>
.file-list-container {
    padding: 5px;
    box-sizing: border-box;
}
.knowledgebase-container {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    background: #fff;
}
.top-slider {
    height: 60px;
    padding: 0 40px;
    align-items: center;
    display: flex;
    justify-content: space-between;
}
.title {
    color: #616161;
    font-size: 38px !important;
    display: flex;
    .kbinfo {
        margin-left: 5px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        .kb_name {
            font-size: 20px;
        }
        .kb_info {
            font-size: 12px;
        }
    }
}
.back-icon {
    margin-right: 5px;
    cursor: pointer;
    font-weight: 900;
}
/deep/ .el-form-item{
        display: flex;
}
/deep/ .el-form-item__content{
    flex: 1;
}
</style>
