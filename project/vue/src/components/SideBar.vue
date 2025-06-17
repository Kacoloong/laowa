<script setup>

</script>

<template>
  <el-aside width="200px" class="sidebar">
  <el-menu>
  <el-menu-item index="1" @click="$router.push('/')">首页</el-menu-item>
  <el-sub-menu index="2">
    <template #title>
      <span>分析</span>
    </template>
    <el-menu-item index="2-1" @click="$router.push('/rebound-analysis')">Rebound分析</el-menu-item>
    <el-menu-item index="2-2" @click="$router.push('/diff-collision')">差分碰撞</el-menu-item>
    <el-menu-item index="2-3" @click="$router.push('/mitm-analysis')">中间相遇</el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="3">
    <template #title>
      <span>设计</span>
    </template>
    <el-sub-menu index="3-1">
      <template #title>
        <span>面向比特</span>
      </template>
      <el-menu-item index="3-1-1" @click="$router.push('/bit-sbox')">生成S盒</el-menu-item>
      <el-menu-item index="3-1-2" @click="$router.push('/bit-algorithm')">具体杂凑算法</el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="3-2" title="面向字">
      <template #title>
        <span>面向字</span>
      </template>
      <el-menu-item index="3-2-1" @click="$router.push('/byte-mds')">生成MDS矩阵</el-menu-item>
      <el-menu-item index="3-2-2" @click="$router.push('/byte-algorithm')">具体杂凑算法</el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  </el-menu>

  </el-aside>
</template>

<style scoped>

.sidebar {
  background-color: #f5f7fa;
  padding: 0px 0;
}
</style>