<template>
  <el-footer class="footer">
    <div class="footer-content">
      <span style="font-size: small">Copyright {{ new Date().getFullYear() }}. All Rights Reserved By {{APP_NAME}}.</span>
    </div>
  </el-footer>
</template>

<script>
import {APP_NAME} from '@/utils/constanst.js'
export default {
  data() {
    return {
      APP_NAME:APP_NAME
    }
  },
}
</script>

<style lang="less" scoped>
.footer {
  background-color: #2c3e50; /* 深色背景 */
  color: #ffffff; /* 白色字体 */
  padding: 10px 0;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
