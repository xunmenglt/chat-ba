<template>
  <div class="home">
    <div class="left-container">
      <div class="title-wrapper">
        <h1 class="system-name" :class="{ 'animate-title': isAnimating }">{{ APP_NAME }}</h1>
        <div class="divider"></div>
        <h2 class="subtitle" :class="{ 'animate-subtitle': isAnimating }">{{ APP_SUB_TITLE }}</h2>
      </div>
      <div class="scientific-features">
        <div class="feature-item">
          <i class="el-icon-cpu feature-icon"></i>
          <span>自然语言处理</span>
        </div>
        <div class="feature-item">
          <i class="el-icon-connection feature-icon"></i>
          <span>知识库构建</span>
        </div>
        <div class="feature-item">
          <i class="el-icon-data-analysis feature-icon"></i>
          <span>AI大模型交互</span>
        </div>
      </div>
    </div>
    <div class="right-container">
      <transition name="fade">
        <div class="login-form-container">
          <el-card class="login-card" shadow="hover">
            <div class="card-header">
              <h2 class="login-title">
                <i class="el-icon-user-solid"></i> 用户认证登录
              </h2>
              <div class="card-subtitle">请输入您的认证信息</div>
            </div>
            <el-form :model="loginForm" ref="loginFormRef" class="login-form">
              <el-form-item label="用户名" prop="username">
                <el-input
                  v-model="loginForm.username"
                  placeholder="科研账号"
                  prefix-icon="el-icon-user"
                  @focus="animateInput('username')"
                  :class="{ 'input-animated': animatedInput === 'username' }"
                />
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input
                  type="password"
                  v-model="loginForm.password"
                  placeholder="访问密码"
                  prefix-icon="el-icon-lock"
                  show-password
                  @focus="animateInput('password')"
                  :class="{ 'input-animated': animatedInput === 'password' }"
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  @click="handleLogin" 
                  class="login-button"
                  icon="el-icon-unlock"
                >
                  授权访问
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </transition>
    </div>
  </div>
</template>

<style lang="less" scoped>
.home {
  background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
              url('@/assets/images/bg.avif');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: space-around;
  color: #ffffff;
  font-family: 'Arial', 'Microsoft YaHei', sans-serif;
}

.left-container {
  text-align: left;
  padding: 0 5%;
  max-width: 600px;
}

.title-wrapper {
  margin-bottom: 40px;
}

.system-name {
  margin: 0;
  font-size: 48px;
  font-weight: bold;
  background: linear-gradient(90deg, #00d2ff, #3a7bd5);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: 1px;
}

.divider {
  height: 3px;
  width: 100px;
  background: linear-gradient(90deg, #00d2ff, #3a7bd5);
  margin: 15px 0;
}

.subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin: 10px 0;
  letter-spacing: 1px;
}

.scientific-features {
  margin-top: 50px;
}

.feature-item {
  display: flex;
  align-items: center;
  margin: 20px 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.feature-icon {
  font-size: 24px;
  margin-right: 15px;
  color: #00d2ff;
}

.animate-title {
  animation: titleGlow 2s infinite alternate;
}

.animate-subtitle {
  animation: subtitleFadeIn 1s ease-in-out forwards;
}

@keyframes titleGlow {
  0% {
    text-shadow: 0 0 5px rgba(0, 210, 255, 0.3);
  }
  100% {
    text-shadow: 0 0 15px rgba(0, 210, 255, 0.7);
  }
}

@keyframes subtitleFadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.right-container {
  padding-right: 5%;
}

.login-form-container {
  margin-top: 20px;
}

.login-card {
  width: 380px;
  padding: 30px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  border: none;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}

.card-header {
  margin-bottom: 25px;
  text-align: center;
}

.login-title {
  margin: 0 0 5px 0;
  font-size: 22px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-title i {
  margin-right: 10px;
  color: #3a7bd5;
}

.card-subtitle {
  font-size: 14px;
  color: #666;
}

.login-form {
  margin-top: 20px;
}

.input-animated {
  animation: pulse 0.5s infinite alternate;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(58, 123, 213, 0.4);
  }
  100% {
    box-shadow: 0 0 0 3px rgba(58, 123, 213, 0);
  }
}

.login-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  letter-spacing: 1px;
  background: linear-gradient(90deg, #00d2ff, #3a7bd5);
  border: none;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(58, 123, 213, 0.4);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>

<script>
import {APP_NAME,APP_SUB_TITLE} from '@/utils/constanst'

export default {
  name: 'HomeView',
  data() {
    return {
      APP_NAME:APP_NAME,
      APP_SUB_TITLE:APP_SUB_TITLE,
      loginForm: {
        username: 'OpenNLG',
        password: 'OpenNLG'
      },
      animatedInput: null,
      isAnimating: true
    };
  },
  mounted() {
    setTimeout(() => {
      this.isAnimating = false;
    }, 3000);
  },
  methods: {
    handleLogin() {
      if (this.loginForm.username === 'OpenNLG' && this.loginForm.password === 'OpenNLG') {
        this.$message.success('认证成功，欢迎访问智核问答系统');
        this.$router.replace('/dashboard');
      } else {
        this.$message.error('认证失败，请检查用户名和密码');
      }
    },
    animateInput(input) {
      this.animatedInput = input;
      setTimeout(() => {
        this.animatedInput = null;
      }, 500);
    }
  }
}
</script>