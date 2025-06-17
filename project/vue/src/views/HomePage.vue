<script setup>
import SideBar from "@/components/SideBar.vue";

</script>
<template>
    <el-container style="height: 100vh;">
        <el-container>
            <SideBar/>
            <el-main class="main-content">
                <h1>杂凑密码自动化设计与分析工具</h1>
            </el-main>
        </el-container>
    </el-container>
</template>

<style scoped>
.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background-color: #0d63d3;
    color: white;
    font-size: 40px;
}
</style>
