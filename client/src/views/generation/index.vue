<template>
    <div class="content-container">
        <div class="tool-container">
            <div class="tool-right">
                <div v-show="false">
                    <v-btn 
                     @click="addUseCase"
                     color="info"
                     elevation="0"
                    >
                        <v-icon>mdi-plus</v-icon>
                        添加用例
                    </v-btn>
                </div>
            </div>
            <div class="tool-left">
                <div class="d-flex flex-row align-center">
                    <div class="filename">{{currentFileInfo.name}}</div>
                    <v-btn @click="fileUploadWinShow=true" color="info" elevation="0"><v-icon>mdi-cloud-upload-outline</v-icon>上传文件</v-btn>
                </div>
            </div>
        </div>
        <el-divider></el-divider>
        <div class="QABox-container">
            <div class="empty" v-if="!qa_box_ids||qa_box_ids.length<=0">
                <el-empty description="暂无测试用例"></el-empty>
              </div>
            <div class="box" v-for="qa_box_id in qa_box_ids" :key="qa_box_id">
                <QABox :qa_box_id="qa_box_id" 
                       :file_name="currentFileInfo.name"
                       :upload_id="upload_id"
                       @deleteItem="deleteUseCase"/>
            </div>
        </div>

        <el-dialog
        :title="'文件上传'"
        :visible.sync="fileUploadWinShow">
            <div class="upload-container">
                <el-upload
                    drag
                    ref="upload"
                    action="#"
                    :on-change="uploadFilehandleChange"
                    :file-list="uplodFileList"
                    :auto-upload="false">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">只能上传pdf文件</div>
                </el-upload>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancleUploadFile">取 消</el-button>
                <el-button type="primary" @click="doUploadFile">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
  
<script>
import generationJS from './index'
export default{
    ...generationJS
}
</script>
  
<style lang="less" scoped>
  @import './index.less';
</style>