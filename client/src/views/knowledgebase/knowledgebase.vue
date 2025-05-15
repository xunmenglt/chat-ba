<template>
  <div class="knowledgebase-container">
    <div class="top-slider d-flex">
      <div class="title">知识库管理</div>
      <v-spacer></v-spacer>
      <div class="opt-container">
        <v-btn @click="createKnowledgeBase" color="primary" elevation="2">
          <v-icon>mdi-plus</v-icon>新建知识库
        </v-btn>
      </div>
    </div>
    <v-divider></v-divider>
    <div class="knowledgebase-list-container">
      <div class="empty" v-if="!data_list || data_list.length <= 0">
        <el-empty description="暂无知识库"></el-empty>
      </div>
      <el-card class="kbitem" v-for="(item) in data_list" :key="item.id" shadow="hover">
        <div class="kb-header">
          <h3 class="kb-title">{{ item.kb_name }}</h3>
          <p class="kb-info">{{ item.kb_info }}</p>
        </div>
        <div class="kb-details">
          <el-tag type="info" size="mini">
            <i class="iconfont icon-embedding"></i>{{ item.embed_model }}
          </el-tag>
          <el-tag type="info" size="mini">
            <i class="iconfont icon-shujuku"></i>{{ item.vs_type }}
          </el-tag>
          <el-tag type="info" size="mini">
            <i class="iconfont icon-wenjian"></i>{{ item.file_count }}
          </el-tag>
          <el-tag type="success" size="mini">{{ item.createTime.split('T').join(" ") }}</el-tag>
        </div>
        <div class="kb-actions">
          <el-button size="mini" type="danger" @click="deletekbdialog=true;deleteKbname=item.kb_name">删除</el-button>
          <el-button size="mini" type="primary" @click="enterKb(item)">进入</el-button>
        </div>
      </el-card>
    </div>

    <!-- 新增知识库表单 -->
    <el-dialog title="新建知识库" :visible.sync="knowledgebasedialog" width="500px" center>
      <el-form :model="create_kb_item" ref="createForm" :rules="formRules">
        <el-form-item label="知识库名*" prop="factory_name">
          <el-input v-model="create_kb_item.factory_name" placeholder="请输入知识库名"></el-input>
        </el-form-item>
        <el-form-item label="知识库描述信息*" prop="info">
          <el-input v-model="create_kb_item.info" placeholder="请输入描述信息"></el-input>
        </el-form-item>
        <el-form-item label="向量数据库*" prop="vector_store_type">
          <el-select v-model="create_kb_item.vector_store_type" placeholder="请选择向量数据库" style="width:100%">
            <el-option v-for="item in vectorStoreList" :key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="向量嵌入模型*" prop="embed_model">
          <el-select v-model="create_kb_item.embed_model" placeholder="请选择嵌入模型" style="width:100%">
            <el-option v-for="item in embeddingModelList" :key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="knowledgebasedialog = false">取 消</el-button>
        <el-button type="primary" @click="doCreateKB">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除弹窗 -->
    <el-dialog title="确认删除" :visible.sync="deletekbdialog" width="400px" center>
      <span>您是否要删除该知识库？此操作将导致所有历史数据被删除，请谨慎操作!</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deletekbdialog = false">取 消</el-button>
        <el-button type="danger" @click="toDeleteKb">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { showTextMessage } from '@/plugins/toastification';
import {
  getKnowledgeBaseListApi,
  createKnowledgeBaseApi,
  getVectorStoreListApi,
  getEmbeddingModelListApi,
  deleteKnowledgeBaseApi
} from '@/utils/api/knowledgebase';

export default {
  data() {
    return {
      data_list: [],
      knowledgebasedialog: false,
      vectorStoreList: [],
      embeddingModelList: [],
      deletekbdialog: false,
      deleteKbname: "",
      create_kb_item: {
        factory_name: "",
        vector_store_type: "",
        embed_model: "",
        info: ""
      },
      formRules: {
        factory_name: [
          { required: true, message: '请输入知识库名', trigger: 'blur' }
        ],
        info: [
          { required: true, message: '请输入描述信息', trigger: 'blur' }
        ],
        vector_store_type: [
          { required: true, message: '请选择向量数据库', trigger: 'change' }
        ],
        embed_model: [
          { required: true, message: '请选择嵌入模型', trigger: 'change' }
        ]
      }
    };
  },
  mounted() {
    this.flashDataList();
    this.init_vector_and_embedding_List();
  },
  methods: {
    async init_vector_and_embedding_List() {
      let vs_res = await getVectorStoreListApi();
      let embed_res = await getEmbeddingModelListApi();
      if (vs_res?.code === 200) {
        this.vectorStoreList = vs_res.data;
      } else {
        showTextMessage('error', '向量数据库列表加载失败');
      }
      if (embed_res?.code === 200) {
        this.embeddingModelList = embed_res.data;
      } else {
        showTextMessage('error', '向量嵌入模型列表加载失败');
      }
    },
    async flashDataList() {
      let response = await getKnowledgeBaseListApi();
      if (response.code === 200) {
        this.data_list = response.data;
      } else {
        showTextMessage('error', `服务器异常：${response.msg}`);
      }
    },
    createKnowledgeBase() {
      this.create_kb_item = {
        factory_name: "",
        vector_store_type: "",
        embed_model: "",
        info: ""
      };
      this.knowledgebasedialog = true;
    },
    async doCreateKB() {
      this.$refs.createForm.validate(async valid => {
        if (valid) {
          this.$modal.loading("知识库创建中...");
          let create_response = await createKnowledgeBaseApi(this.create_kb_item);
          if (create_response?.code === 200) {
            showTextMessage("success", create_response.msg);
            this.flashDataList().then(() => {
              this.knowledgebasedialog = false;
            });
          } else {
            showTextMessage("error", create_response.msg);
          }
          this.$modal.closeLoading();
        } else {
          showTextMessage("error", "请检查表单填写是否完整");
        }
      });
    },
    async toDeleteKb() {
      let response = await deleteKnowledgeBaseApi(this.deleteKbname);
      if (response?.code === 200) {
        showTextMessage('success', response.msg);
        this.flashDataList().then(() => {
          this.deletekbdialog = false;
        });
      } else {
        showTextMessage('error', response.msg);
      }
    },
    enterKb(item) {
      this.$router.push({ path: '/dashboard/knowledgebase/filemanage', query: item });
    }
  }
};
</script>

<style lang="less" scoped>
@main-color: #2c3e50;
@accent-color: #3498db;
@bg-color: #f7f9fc;

.knowledgebase-container {
  background-color: @bg-color;
  padding: 20px;
  border-radius: 8px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.top-slider {
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
  background-color: @main-color;
  color: white;
  border-radius: 8px 8px 0 0;
}

.title {
  font-size: 24px;
  font-weight: bold;
}

.knowledgebase-list-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
  padding-bottom: 40px;
}

.kbitem {
  width: calc(25% - 20px);
  min-width: 250px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}

.kbitem:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.kb-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.kb-title {
  font-size: 16px;
  font-weight: bold;
  color: @main-color;
  margin: 0;
}

.kb-info {
  font-size: 13px;
  color: #888;
  margin-top: 5px;
}

.kb-details {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 15px;
}

.kb-details .el-tag {
  font-size: 12px;
}

.kb-actions {
  padding: 10px 15px;
  text-align: right;
}

.empty {
  width: 100%;
  text-align: center;
  margin-top: 40px;
}
</style>