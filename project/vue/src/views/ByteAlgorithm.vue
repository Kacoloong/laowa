<script setup>
import ByteAlgorithmDisplay from "@/components/ByteAlgorithmDisplay.vue";
import SideBar from "@/components/SideBar.vue";
// import HeaderBar from "@/components/HeaderBar.vue";
</script>

<template>
  <el-header class="header">
      <div class="header-title">杂凑密码自动化设计与分析工具 - 面向字节的设计</div>
  </el-header>
  <el-container>
    <SideBar/>
    <el-main style="padding: 15px;">
      <ByteAlgorithmDisplay/>
      <el-form-item class="button-group">
        <div class="btn-wrapper">
          <el-button type="primary" @click="$router.push('/')" class="action-btn">返回主页</el-button>
        </div>
      </el-form-item>
    </el-main>
  </el-container>
</template>

<style scoped>
.button-group {
  display: flex;
  justify-content: flex-start;
  padding-left: 120px;
  margin-top: 20px;
}

.btn-wrapper {
  display: flex;
  gap: 150px;
}

.action-btn {
  font-size: 15px;
  padding: 12px 24px;
}

.header {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    background-color: #0d63d3;
    color: white;
    height: 100px;
}

.header-title {
    font-weight: bold;
}

</style>
