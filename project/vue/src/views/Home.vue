<template>
    <el-container style="height: 100vh;">
        <el-container>
            <el-aside width="200px" class="sidebar">
                <el-menu>
                    <el-menu-item index="1" @click="$router.push('/')">首页</el-menu-item>
                    <el-sub-menu index="2">
                        <template #title>
                            <el-icon><location /></el-icon>
                            <span>分析</span>
                        </template>
                        <el-menu-item index="2-1" @click="$router.push('/rebound-analysis')">Rebound分析</el-menu-item>
                        <el-menu-item index="2-2" @click="$router.push('/mitm-analysis')">中间相遇原像分析</el-menu-item>
                        <el-menu-item index="2-3">差分碰撞</el-menu-item>
                    </el-sub-menu>
                    <el-sub-menu index="3">
                        <template #title>
                            <el-icon><location /></el-icon>
                            <span>设计</span>
                        </template>
                        <el-menu-item index="3-1">面向比特</el-menu-item>
                        <el-menu-item index="3-2">面向字</el-menu-item>
                    </el-sub-menu>
                </el-menu>
            </el-aside>
            <el-main class="main-content">
                <h1>杂凑密码自动化设计与分析工具</h1>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    name: 'HomePage'
};
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    background-color: #0d63d3;
    color: white;
    height: 150px;
}

.header-title {
    font-weight: bold;
}

.sidebar {
    background-color: #f5f7fa;
    padding: 0px 0;
}

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
