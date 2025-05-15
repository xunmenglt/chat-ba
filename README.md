# Chat-BA 项目简介

**Chat-BA** 是一个基于大语言模型的知识库问答系统（KBQA），允许用户上传文档、构建知识库，并通过自然语言提问获取相关信息。系统集成了文档处理、向量存储和语言模型，能够基于上传的知识文档提供有效的答案。

---

## ✨ 主要功能

- **知识库管理**：创建、查看和删除知识库
- **文档上传与处理**：支持 PDF、DOCX、TXT、JSONL 等格式
- **自然语言查询**：使用大语言模型提问并获取答案
- **来源引用**：展示答案出处，便于验证
- **模型选择**：支持本地模型与 API 模型的切换使用

---

## 🏗️ 系统架构

```text
LLM 层
 └─ 本地模型 / 外部 API 模型

知识处理层
 ├─ 嵌入模型（bge-large-zh）
 ├─ 文档处理器（加载器、分割器）
 └─ 向量数据库（Qdrant）

API 层
 └─ FastAPI 接口（聊天、问答、文件管理）

客户端层
 └─ Vue + Element UI Web 前端
````

---

## 🔧 技术栈

* **前端**：Vue.js, Element UI, Vuetify, Node20.x
* **后端**：Python 3.9, FastAPI, LangChain
* **数据库**：SQLite
* **向量库**：Qdrant
* **嵌入模型**：BGE-large-zh
* **支持模型**：

  * 本地模型：ChatGLM3、Qwen 系列等
  * API 模型：千帆 API、OpenAI API 等

---

## 🚀 快速开始

### 环境要求

* Python 3.9
* Node.js 20.x

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/xunmenglt/chat-ba.git  
cd chat-ba

# 安装后端依赖
cd server  
conda activate -n chatba python=3.9  
pip install -r requirements.txt

# 安装前端依赖
cd ../client  
# 如果未安装nvm，请先安装
nvm use 20 
# 配置淘宝镜像源（可选）
npm config set registry https://registry.npmmirror.com
npm install
```

### 启动项目

```bash
# 启动后端服务
cd server
./run.sh

# 启动前端服务
cd ../client
npm run serve
```

### 访问系统

浏览器打开：`http://localhost:8080`

---

## 📘 使用指南

### 创建知识库

1. 打开设置面板创建新知识库
2. 上传文档（PDF、DOCX、TXT、JSONL）
3. 系统自动处理并建立向量索引

### 查询知识库

1. 选择知识库 `retrieval.vue:396-400`
2. 选择语言模型
3. 输入自然语言问题 `retrieval.vue:182-184`
4. 返回答案及来源文档 `retrieval.vue:144-150`

### 高级设置

* **模板选择**：设置提示模板 `retrieval.vue:247`
* **文档匹配数量**：控制返回数量 `retrieval.vue:240`
* **相似度阈值**：设置匹配精度 `retrieval.vue:242`
* **LLM 参数**：温度、top\_p、max\_tokens `retrieval.vue:241-246`
* **流式输出**：开启/关闭流式响应 `retrieval.vue:243`

### 文件预览功能

| 类型    | 方法位置                      |
| ----- | ------------------------- |
| PDF   | `fileController.py:19-30` |
| QA 文件 | `fileController.py:32-43` |
| 文本文件  | `fileController.py:45-56` |

---

## 📂 项目结构

```text
chat-ba/  
├── client/                 # 前端代码  
│   ├── src/  
│   │   ├── views/          # 页面视图  
│   │   │   └── retrieval/  # 问答检索页  
│   │   ├── components/     # 公共组件  
│   │   ├── utils/          # 工具函数  
│   │   └── assets/         # 静态资源  
├── server/                 # 后端服务  
│   ├── server/  
│   │   ├── controller/     # 接口控制器  
│   │   ├── db/             # 数据库逻辑  
│   │   │   ├── mapper/     # ORM 映射  
│   │   │   └── models/     # 数据模型  
│   │   ├── services/       # 核心业务逻辑  
│   │   └── utils/          # 工具模块  
│   ├── configs/            # 配置项  
│   ├── lib/                # 第三方库封装  
│   └── requirements.txt    # 后端依赖  
└── README.md
```

---

## 💬 聊天功能说明

* 用户提问后调用后端服务 `retrieval.vue:404-420`
* 实时展示回答 `retrieval.vue:423-433`
* 展示来源文档 `retrieval.vue:434-446`

---

## 🤝 贡献指南

欢迎贡献：

1. Fork 本仓库
2. 创建分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add some amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request
---

## 📬 联系方式

项目维护者：寻梦

邮箱：xmliuteng@163.com

---

感谢使用 **Chat-BA**！希望这个工具能帮助您更高效地管理和查询知识库内容。
