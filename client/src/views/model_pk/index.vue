<template>
    <div class="content-container">
        <div class="tool-container">
            <div class="tool-right">
                <div class="d-flex flex-row align-center">
                    <div class="opt-item" v-if="modelBoxList&&modelBoxList.length<4" @click="handlerAddModel">
                        <v-btn depressed dark color="purple">
                            <i class="iconfont icon-icon_pk"></i>添加模型
                        </v-btn>
                    </div>
                </div>
            </div>
            <div class="tool-left">
                <div class="d-flex flex-row align-center">
                    <div class="opt-item"  v-if="showCreateReport">
                        <v-btn @click="createReport" depressed dark color="#5865f2" size="small" variant="flat">
                            <i class="iconfont icon-pingjiabaogao"></i> 生成报告
                        </v-btn>
                    </div>
                </div>
            </div>
        </div>
        <div class="modelpk-container">
            <PK v-if="!modelBoxList || modelBoxList.length==0"></PK>
            <div v-for="item in modelBoxList" :key="item.id" class="model-container">
                <ChatBox :ref="`model-${item.id}`" @handleDeleteModelItem="handleDeleteModelItem" :model="item" />
            </div>
        </div>
        <div class="query-input">
            <div id="textarea-with-actions-container">
                <el-input ref="chatInputRef" @keyup.native="onKeyUpSend" @blur="handleInputBlur"
                    @focus="handleInputFocus" type="textarea" :rows="1" resize="none"
                    placeholder="请输入问题 ctrl + enter 发送" v-model="query">
                </el-input>
                <div class="opt-item" @click="handleSubmitForm">
                    <i class="icon el-icon-s-promotion"></i>
                </div>
            </div>
        </div>
        <!-- 新建模型 -->
        <el-dialog title="创建模型" label-width="50" label-position="right" size="small" :visible.sync="add_dialogVisible"
            width="40%" :close-on-click-modal="false">
            <el-form>
                <el-form-item label="模型">
                    <el-select size="mini" v-model="modelItemTemp.model_name" placeholder="请选择模型">
                        <el-option v-for="item in modelList" :key="item" :label="item" :value="item"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="历史对话数">
                    <el-input-number size="mini" class="item" v-model="modelItemTemp.history_len" :min="1"
                        :max="10"></el-input-number>
                </el-form-item>
                <el-form-item label="最大推理长度">
                    <el-slider class="item" v-model="max_tokens" :format-tooltip="formatMax_tokens"></el-slider>
                </el-form-item>
                <el-form-item label="Temperature">
                    <el-slider class="item" v-model="temperature" :format-tooltip="formatTemperature"></el-slider>
                </el-form-item>
                <el-form-item label="TopP">
                    <el-slider class="item" v-model="top_p" :format-tooltip="formatTop_p"></el-slider>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="add_dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addModel">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 新建模型 -->
        <el-dialog title="评估报告" label-width="50" label-position="right" size="small" :visible.sync="showReport"
            width="90%" :close-on-click-modal="false">
            <el-table :data="reportDate" style="width: 100%">
                <el-table-column prop="model_name" label="模型名称" width="180">
                </el-table-column>
                <el-table-column prop="temperature" label="温度" width="180">
                </el-table-column>
                <el-table-column prop="top_p" label="top-p">
                </el-table-column>
                <el-table-column prop="total_input_tokens" label="输入总token数">
                </el-table-column>
                <el-table-column prop="total_output_tokens" label="输出总token数">
                </el-table-column>
                <el-table-column prop="total_time" label="总耗时">
                </el-table-column>
                <el-table-column prop="avg_token_output_speed" label="推理速度(tokens/s)">
                </el-table-column>
                <el-table-column prop="score" label="评分(GPT-4)">
                </el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="showReport = false">取 消</el-button>
                <el-button type="primary" @click="flashReport">重新生成</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import indexJS from './index'
export default{
    ...indexJS
}
</script>
  
<style lang="less" scoped>
    @import './index.less';
</style>