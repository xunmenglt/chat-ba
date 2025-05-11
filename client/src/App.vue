<template>
  <v-app>
    <v-main class="main-container">
      <router-view />
    </v-main>
    <Foot />
  </v-app>

</template>


<script>
import Foot from '@/components/foot'

export default {
  name: "App",
  components: {
    Foot
  }
}
</script>

<style lang="less">

/* 整个滚动条 */
::-webkit-scrollbar {
  width: 5px;
  /* 滚动条的宽度 */
  height: 10px;
  /* 滚动条的高度，对水平滚动条有效 */
  position: absolute;
}

/* 滚动条轨道 */
::-webkit-scrollbar-track {
  border-radius: 10px;
}

/* 滚动条滑块 */
::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-color: #c1c1c1;
  /* 滑块的背景颜色 */
  border: 3px solid #e1e1e1;
  /* 滑块的边框和轨道相同的颜色，可以制造“边距”的效果 */
}

::-webkit-scrollbar-thumb:hover {
  background-color: #d4d4d4;
  /* 滑块的悬停颜色 */
}

::-webkit-scrollbar-thumb:active {
  background-color: #d3d3d3;
  /* 滑块的激活颜色 */
}
</style>
