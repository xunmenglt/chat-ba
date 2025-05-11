<template>
  <div class="home">
    <div class="left-container">
      <h1 class="system-name" :class="{ 'animate-title': isAnimating }">{{APP_NAME}}</h1>
      <h2 class="subtitle" :class="{ 'animate-subtitle': isAnimating }">{{APP_SUB_TITLE}}</h2>
    </div>
    <div class="right-container">
      <transition name="fade">
        <div class="login-form-container">
          <el-card class="login-card" shadow="hover">
            <h2 class="login-title">用户登录</h2>
            <el-form :model="loginForm" ref="loginFormRef" class="login-form">
              <el-form-item label="用户名" prop="username">
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入用户名"
                  prefix-icon="el-icon-user"
                  @focus="animateInput('username')"
                  :class="{ 'input-animated': animatedInput === 'username' }"
                />
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input
                  type="password"
                  v-model="loginForm.password"
                  placeholder="请输入密码"
                  prefix-icon="el-icon-lock"
                  @focus="animateInput('password')"
                  :class="{ 'input-animated': animatedInput === 'password' }"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleLogin" class="login-button">登录</el-button>
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
  background: linear-gradient(135deg, #2c3e50, #34495e);
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: space-around;
  color: #ecf0f1;
}

.left-container {
  text-align: left;
  padding-left: 20px;
  margin-right: 20px;
}

.system-name {
  margin: 10px 0;
  font-size: 64px; /* 增大字体尺寸 */
  font-weight: bold;
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease;
}

.subtitle {
  font-size: 32px; /* 增大副标题字体尺寸 */
  color: #bdc3c7;
}

.animate-title {
  animation: titleBounce 0.5s infinite alternate;
}

.animate-subtitle {
  animation: subtitleFadeIn 0.5s ease-in-out forwards;
}

@keyframes titleBounce {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-10px);
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
  padding-right: 20px;
}

.login-form-container {
  margin-top: 20px;
}

.login-card {
  width: 400px;
  padding: 20px;
  border-radius: 15px;
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.login-card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.login-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #34495e;
}

.login-form {
  max-width: 400px;
}

.input-animated {
  animation: pulse 0.5s infinite alternate;
}

@keyframes pulse {
  0% {
    border-color: #3498db;
  }
  100% {
    border-color: #2980b9;
  }
}

.login-button {
  width: 100%;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
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
        username: '',
        password: ''
      },
      animatedInput: null,
      isAnimating: true
    };
  },
  mounted() {
    setTimeout(() => {
      this.isAnimating = false;
    }, 3000); // 动画持续3秒
  },
  methods: {
    handleLogin() {
      if (this.loginForm.username && this.loginForm.password) {
        this.$modal.msgSuccess("登录成功")
        // 此处可以添加导航逻辑
        this.$router.replace('/dashboard')
      } else {
        this.$modal.msgWarning("请输入用户名或密码")
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
