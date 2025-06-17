<!-- <template>
  <el-container style="height: 100vh;">
    <el-aside width="50%" style="background-color: #f5f5f5; padding: 20px;">
      <cipher-form />
    </el-aside>
    <el-main width="50%" style="padding: 20px;">
      <rebound-analysis />
    </el-main>
  </el-container>
</template>

<script>
import CipherForm from './views/CipherForm.vue';
import ReboundAnalysis from './views/ReboundAnalysis.vue';

export default {
  name: 'App',
  components: {
    CipherForm,
    ReboundAnalysis,
  },
};
</script>

<style>
.el-aside,
.el-main {
  height: 100%;
}
</style> -->

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  height: 100vh;
}
</style>
