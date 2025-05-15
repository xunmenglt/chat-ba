<template>
  <div class="dashboard-container" id="dashboard-container">
    <el-header class="app-bar">
      <div class="logo-container" @click="toHome">
        <h1 class="software-name">
          <i class="el-icon-cpu"></i>
          {{APP_NAME}}
        </h1>
      </div>
      <div class="header-right">
        <div class="current-module">
          <i :class="currentTab.icon" class="module-icon"></i>
          <span class="module-name">{{ currentTab.label }}</span>
        </div>
        <el-dropdown class="user-dropdown">
          <span class="el-dropdown-link">
            <el-avatar :size="36" style="background-color: #3498db" :src="avater">
            </el-avatar>
            <span class="user-name">系统用户</span>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <!-- <el-dropdown-item>
              <i class="el-icon-user"></i>个人中心
            </el-dropdown-item>
            <el-dropdown-item>
              <i class="el-icon-setting"></i>系统设置
            </el-dropdown-item> -->
            <el-dropdown-item divided @click.native="logout">
              <i class="el-icon-switch-button"></i>退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-header>
    
    <div class="layout-container">
      <el-menu 
        :default-active="activeMenu"
        @select="menuHandler"
        :collapse="isCollapse"
        class="side-menu"
        background-color="#2c3e50"
        text-color="#bdc3c7"
        active-text-color="#3498db">
        
        <!-- <div class="menu-collapse" @click="isCollapse=!isCollapse">
          <i class="el-icon-s-fold" v-if="!isCollapse"></i>
          <i class="el-icon-s-unfold" v-else></i>
        </div> -->
        
        <el-menu-item 
          v-for="(tab) in tabs" 
          :key="tab.path" 
          :index="tab.path"
          class="menu-item">
          <i :class="tab.icon" class="menu-icon"></i>
          <span slot="title">{{ tab.label }}</span>
          <el-tag v-if="tab.badge" size="mini" type="danger">{{tab.badge}}</el-tag>
        </el-menu-item>
      </el-menu>

      <el-main class="main-container">
        <div class="content-wrapper">
          <router-view />
        </div>
      </el-main>
    </div>
  </div>
</template>

<script>
import {APP_NAME} from '@/utils/constanst'
export default {
  data() {
    return {
      APP_NAME: APP_NAME,
      isCollapse: false,
      avater:require('@/assets/logos/avatar.png'),
      tabs: [
        { 
          path: '/dashboard/knowledgebase', 
          label: '知识库管理', 
          icon: 'el-icon-notebook-2',
        },
        { 
          path: '/dashboard/chat', 
          label: '智能对话', 
          icon: 'el-icon-chat-line-round' 
        },
        { 
          path: '/dashboard/retrieval', 
          label: '知识检索', 
          icon: 'el-icon-search' 
        },
        // { 
        //   path: '/dashboard/generation', 
        //   label: '数据生成', 
        //   icon: 'el-icon-data-line' 
        // },
        // { 
        //   path: '/dashboard/model_pk', 
        //   label: '模型对比', 
        //   icon: 'el-icon-cpu' 
        // },
      ],
    };
  },
  computed: {
    activeMenu() {
      return this.$route.path;
    },
    currentTab() {
      return this.tabs.find(tab => tab.path === this.$route.path) || this.tabs[0];
    }
  },
  methods: {
    toHome() {
      this.$router.push('/');
    },
    menuHandler(path) {
      if (path !== this.$route.path) {
        this.$router.push(path);
      }
    },
    logout() {
      this.$confirm('确定要退出系统吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$router.push('/');
        this.$message.success('已安全退出系统');
      });
    }
  }
};
</script>

<style lang="less" scoped>
.dashboard-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: #f5f7fa;
}

.app-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 60px !important;
  background: linear-gradient(135deg, #2c3e50, #34495e) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  color: white;
  z-index: 10;
  
  .logo-container {
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      opacity: 0.8;
    }
    
    .software-name {
      margin: 0;
      font-size: 20px;
      font-weight: 500;
      display: flex;
      align-items: center;
      
      i {
        margin-right: 10px;
        font-size: 24px;
        color: #3498db;
      }
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    
    .current-module {
      display: flex;
      align-items: center;
      margin-right: 30px;
      padding: 5px 15px;
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      
      .module-icon {
        margin-right: 8px;
        font-size: 18px;
        color: #3498db;
      }
      
      .module-name {
        font-size: 16px;
        font-weight: 500;
      }
    }
    
    .user-dropdown {
      cursor: pointer;
      
      .el-dropdown-link {
        display: flex;
        align-items: center;
        
        .user-name {
          margin: 0 8px 0 12px;
          font-size: 14px;
        }
      }
    }
  }
}

.layout-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.side-menu {
  height: 100%;
  border-right: none !important;
  transition: width 0.3s;
  position: relative;
  
  &:not(.el-menu--collapse) {
    width: 220px !important;
  }
  
  &.el-menu--collapse {
    width: 64px !important;
  }
  
  .menu-collapse {
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #bdc3c7;
    font-size: 20px;
    transition: all 0.3s;
    
    &:hover {
      color: #3498db;
      background-color: rgba(52, 152, 219, 0.1);
    }
  }
  
  .menu-item {
    height: 56px;
    line-height: 56px;
    margin: 4px 0;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    
    &:hover {
      background-color: rgba(52, 152, 219, 0.1) !important;
      color: #3498db !important;
      
      .menu-icon {
        color: #3498db !important;
      }
    }
    
    .menu-icon {
      font-size: 18px;
      margin-right: 10px;
      color: #bdc3c7;
    }
    
    .el-tag {
      position: absolute;
      right: 20px;
      top: 16px;
    }
  }
  
  .el-menu-item.is-active {
    background-color: rgba(52, 152, 219, 0.2) !important;
    color: #3498db !important;
    font-weight: 500;
    
    .menu-icon {
      color: #3498db !important;
    }
  }
}

.main-container {
  flex: 1;
  padding: 0 !important;
  overflow: hidden;
  background-color: #f5f7fa;
  
  .content-wrapper {
    height: 100%;
    padding: 20px;
    overflow-y: auto;
    background-color: white;
    border-radius: 8px 0 0 0;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  }
}

// 响应式调整
@media screen and (max-width: 768px) {
  .app-bar {
    padding: 0 15px;
    
    .header-right {
      .current-module {
        display: none;
      }
    }
  }
  
  .side-menu:not(.el-menu--collapse) {
    width: 180px !important;
  }
}
</style>