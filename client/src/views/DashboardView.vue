<template>
    <div class="dashboard-container" id="dashboard-container">
      <el-header class="app-bar" style="background-color: #34495e; color: white;">
        <div class="logo-container" @click="toHome">
          <h1 class="software-name">{{APP_NAME}}</h1>
        </div>
        <div class="tip-text">{{ menu_tag }}</div>
        
      </el-header>
      <div class="layout-container">
        
        <el-menu 
            :default-active="filteredTabs[0].path"
            @select="menuHandler"
            :collapse="isCollapse"
            background-color="#575c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <!-- <el-input v-model="searchQuery" placeholder="搜索菜单" @input="filterTabs" class="search-input"></el-input> -->
            <div class="collapse" :class="{'close':isCollapse}" @click="isCollapse=!isCollapse">
                <i class="el-icon-arrow-right" v-if="isCollapse"></i>
                <i class="el-icon-arrow-left" v-else></i>
            </div>
            <el-menu-item v-for="(tab) in filteredTabs" :key="tab.path" :index="tab.path">
                <i class="mdi" :class="tab.icon" style="margin-right:5px"></i>
                <span slot="title">{{ tab.label }}</span>
            </el-menu-item>
        </el-menu>

        <el-container class="fun-container">
          <router-view />
        </el-container>
      </div>
    </div>
  </template>
  
  <script>
  import {APP_NAME} from '@/utils/constanst'
  export default {
    data() {
      return {
        menu_tag: '知识库',
        tabItem: '',
        drawer: true,
        searchQuery: '',
        isCollapse: false,
        APP_NAME:APP_NAME,
        tabs: [
          { path: '/dashboard/knowledgebase', label: '知识库', icon: 'mdi-book' },
          { path: '/dashboard/chat', label: '聊天对话', icon: 'mdi-message' },
          { path: '/dashboard/retrieval', label: '检索问答', icon: 'mdi-magnify' },
          { path: '/dashboard/generation', label: '数据生成', icon: 'mdi-content-paste' },
          { path: '/dashboard/model_pk', label: '模型对战', icon: 'mdi-robot' },
          // { path: '/dashboard/report_extraction', label: '行业报告抽取', icon: 'mdi-file-document' },
        ],
        filteredTabs: [],
      };
    },
    created() {
      this.tabItem = this.$route.path;
      this.filteredTabs = this.tabs;
    },
    methods: {
      toHome() {
        this.$router.push('/');
      },
      menuHandler(path) {
        if (path !== this.$route.path) {
          this.menu_tag = this.tabs.find(tab => tab.path === path).label;
          this.$router.push(path);
        }
      },
      filterTabs() {
        const query = this.searchQuery.toLowerCase();
        this.filteredTabs = this.tabs.filter(tab => 
          tab.label.toLowerCase().includes(query)
        );
      },
    },
  };
  </script>
  
  <style lang="less" scoped>
  .dashboard-container {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .layout-container {
    display: flex;
    position: relative;
    height: calc(100% - 64px);
  }
  
  .fun-container {
    flex: 1;
    padding: 6px;
  }
  .app-bar{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  /deep/ .el-menu{
    padding-left: 0 !important;
  }
  .collapse{
    position: absolute;
    font-size: 40px;
    color: rgb(225, 214, 198);
    z-index: 1;
    font-weight: 900;
    transform: translateX(60%);
    top: 40%;
    right: 0;
    cursor: pointer;
    display: none;
  }
  .el-menu{
    position: relative;
  }
  .el-menu:hover{
    .collapse{
        display: block;
    }
  }
  </style>
  