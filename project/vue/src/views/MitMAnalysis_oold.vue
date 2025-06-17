<template>
    <el-header class="header">
        <div class="header-title">杂凑密码自动化设计与分析工具 - SHA-3类杂凑密码中间相遇原像分析</div>
    </el-header>
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
                    <el-menu-item index="2-2">差分碰撞</el-menu-item>
                    <el-menu-item index="2-3" @click="$router.push('/mitm-analysis')">中间相遇</el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-aside>
        <el-main style="padding: 10px;">
            <el-row :gutter="20" justify="center">
                <el-col :span="14">
                    <!-- 内容居中 -->
                    <div class="content-center">
                        <el-row justify="center"> <!-- 新增行使得整个表单居中 -->
                            <el-col :span="24">
                                <el-form label-width="150px" class="centered-form" :model="{ rounds: rounds, z_size: z_size, obj_value: obj_value,k_i1:k_i1,k_i2:k_i2,k_i3:k_i3 }">
                                    <el-row justify="center" :gutter="0">
                                        <el-col :span="8">
                                            <el-form-item label="轮数" prop="rounds" :rules="[{ validator: validateRounds, trigger: 'blur' }]">
                                                <el-input v-model="rounds" placeholder="请输入轮数"></el-input>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="lane的大小" prop="z_size" :rules="[{ validator: validateZSize, trigger: 'blur' }]">
                                                <el-input v-model="z_size" placeholder="请输入lane的大小"></el-input>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="匹配点的值" prop="obj_value" :rules="[{ validator: validateObjValue, trigger: 'blur' }]">
                                                <el-input v-model="obj_value" placeholder="请输入匹配点的值"></el-input>
                                            </el-form-item>
                                        </el-col>
                                    </el-row>
                                    <el-row justify="center" :gutter="0">
                                        <el-col :span="8">
                                            <el-form-item label="S盒下标参数k1" prop="k_i1" :rules="[{ validator: validatek1, trigger: 'blur' }]">
                                                <el-input v-model="k_i1" placeholder="请输入k1的值"></el-input>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="S盒下标参数k2" prop="k_i2" :rules="[{ validator: validatek2, trigger: 'blur' }]">
                                                <el-input v-model="k_i2" placeholder="请输入k2的值"></el-input>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="S盒下标参数k3" prop="k_i3" :rules="[{ validator: validatek3, trigger: 'blur' }]">
                                                <el-input v-model="k_i3" placeholder="请输入k3的值"></el-input>
                                            </el-form-item>
                                        </el-col>
                                    </el-row>

                                    <!-- 居中对齐的 rho 5x5 数组输入 -->
                                    <el-row justify="center" style="margin-top: 10px; text-align: center;">
                                        <el-col :span="24">
                                            <h3>循环移位值</h3>
                                        </el-col>
                                        <el-col :span="12">
                                            <el-row justify="center" v-for="(row, rowIndex) in rho_values" :key="rowIndex" :gutter="10">
                                                <el-col v-for="(value, colIndex) in row" :key="colIndex" :span="4">
                                                    <el-input v-model="rho_values[rowIndex][colIndex]" placeholder="值" type="number"></el-input>
                                                </el-col>
                                            </el-row>
                                        </el-col>
                                    </el-row>

                                    <!-- 按钮组位于5x5数组下方居中 -->
                                    <el-row justify="center" style="margin-top: 10px;">
                                        <el-button type="primary" @click="analyze" style="margin: 0 10px;">开始分析</el-button>
                                        <el-button type="success" @click="generateChart" style="margin: 0 10px;">生成结果图</el-button>
                                        <el-button type="danger" @click="cancelAnalysis" style="margin: 0 10px;">取消分析</el-button>
                                    </el-row>
                                </el-form>
                            </el-col>
                        </el-row>

                        <!-- 分析结果显示，居中 -->
                        <el-row justify="center" style="margin-top: 20px;">
                            <el-col :span="20">
                                <el-card class="box-card scrollable" ref="resultsContainer">
                                    <h2>分析结果:</h2>
                                    <div v-html="renderedResult" class="pre-wrap reduced-line-height"></div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </div>
                </el-col>
                <el-col :span="10">
                    <div class="image-container">
                        <iframe :src="pdfSrc" width="800" height="1000"></iframe>
                    </div>
                </el-col>
            </el-row>
        </el-main>

    </el-container>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid'; // 引入 UUID 库生成 task_id
export default {
    setup() {
        const rounds = ref(4);
        // 定义自定义验证函数
        const validateRounds = (rule, value, callback) => {
            if (value <= 2) {
                callback(new Error("轮数要大于2"));
            } else {
                callback(); // 验证通过
            }
        };
        const validatek1 = (rule, value, callback) => {
            if (value < 0 || value > 4) {
                callback(new Error("S盒下标参数k1的值必须在0到4之间"));
            } else {
                callback(); // 验证通过
            }
        };
        const validatek2 = (rule, value, callback) => {
            if (value < 0 || value > 4) {
                callback(new Error("S盒下标参数k2的值必须在0到4之间"));
            } else {
                callback(); // 验证通过
            }
        };
        const validatek3 = (rule, value, callback) => {
            if (value < 0 || value > 4) {
                callback(new Error("S盒下标参数k3的值必须在0到4之间"));
            } else {
                callback(); // 验证通过
            }
        };
        const z_size = ref(64);
        const obj_value = ref(1);
        const k_i1 = ref(0);
        const k_i2 = ref(1);
        const k_i3 = ref(2);
        // 验证 z_size 只能为 32 或 64
        const validateZSize = (rule, value, callback) => {
            const numericValue = Number(value); 
            if (numericValue  !== 32 && numericValue  !== 64) {
                callback(new Error("lane的大小只能为32或64"));
            } else {
                callback();
            }
        };

        // 验证 obj_value 必须大于 0
        const validateObjValue = (rule, value, callback) => {
            if (value <= 0) {
                callback(new Error("匹配点的值必须大于0"));
            } else {
                callback();
            }
        };
        const rho_values = ref([
            [0, 36, 3, 41, 18],
            [1, 44, 10, 45, 2],
            [62, 6, 43, 15, 61],
            [28, 55, 25, 21, 56],
            [27, 20, 39, 8, 14]
        ]);
        
        const pdfSrc = ref('');
        const renderedResult = ref('');
        const pdfFilePath = ref('');  // 将 pdfFilePath 定义为 ref
        const currentTaskId = ref(null); // 用于存储当前分析任务的 ID

        const analyze = async () => {
            // 每次分析前清空结果区域
            renderedResult.value = '';
            try {
                currentTaskId.value = uuidv4(); // 生成唯一的 task_id
                const response = await axios.post('http://127.0.0.1:5000/mitm-analysis', {
                    rounds: parseInt(rounds.value, 10),  // 确保是整数
                    z_size: parseInt(z_size.value, 10),  // 转换 z_size 为整数
                    obj_value: parseInt(obj_value.value, 10),  // 转换 obj_value 为整数
                    rho_values: rho_values.value,  // 这个已经是数组
                    task_id: currentTaskId.value ,// 将 task_id 发送到后端
                    k_i1: parseInt(k_i1.value, 10),
                    k_i2: parseInt(k_i2.value, 10),
                    k_i3: parseInt(k_i3.value, 10)
                },{
                    headers: {
                        'Content-Type': 'application/json'
                            }                    
                });
                const data = response.data;
                // 确保返回的对象包含 pdf_file 字段
                if (data.pdf_file) {
                    pdfFilePath.value = data.pdf_file; // 正确赋值
                    console.log('PDF file path set to:', pdfFilePath.value);
                } else {
                    console.error('PDF file path not found in response.');
                }
                // 格式化返回结果
                renderedResult.value = `
                    <p><strong>状态:</strong> ${data.status}</p>
                    <p><strong>开始时间:</strong> ${data.start_time}</p>
                    <p><strong>结束时间:</strong> ${data.end_time}</p>
                    <p><strong>耗时:</strong> ${data.elapsed_time} 秒</p>
                    <p><strong>pdf文件路径:</strong> ${data.pdf_file}</p>
                    <p><strong>TikZ文件路径:</strong> ${data.tikz_file}</p>
                `;
                
                // // 保存 PDF 文件路径供生成图按钮使用
                // pdfFilePath.value = data.pdf_file;
                
            } catch (error) {
                renderedResult.value = `分析失败：${error.message}`;
            }
};
        const generateChart = () => {
            if (!pdfFilePath.value) {
                renderedResult.value = "请先运行分析，然后再生成图。";
                return;
            }
            pdfSrc.value = `http://127.0.0.1:5000/get-pdf?filePath=${encodeURIComponent(pdfFilePath.value)}`;
            console.log("PDF Src set to:", pdfSrc.value);
        };
        const cancelAnalysis = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:5000/cancel-analysis', {
                    task_id: currentTaskId  // 假设 `currentTaskId` 是当前任务的 ID
                });
                if (response.data.status === 'canceled') {
                    alert("分析已取消");
                    currentTaskId.value = null; // 重置任务 ID
                } else {
                    alert("取消分析失败：" + response.data.message);
                }
            } catch (error) {
                console.error("取消分析出错", error);
            }
        };

        return {
            rounds,
            validateRounds,
            validatek1,
            validatek2,
            validatek3,
            z_size,
            obj_value,
            k_i1,
            k_i2,
            k_i3,
            rho_values,
            pdfSrc,
            renderedResult,
            analyze,
            generateChart,
            cancelAnalysis,
            validateZSize,
            validateObjValue
        };
    }
};
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    background-color: #0d63d3;
    color: white;
    height: 100px;
}

.sidebar {
    background-color: #f5f7fa;
}

.centered-form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.button-group {
    display: flex;
    justify-content: center;
    gap: 20px;
}

.image-container {
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #dcdcdc;
    padding: 20px;
    min-height: 500px;
}

.box-card {
    margin-top: 30px;
    min-height: 300px;
    max-width: 800px;
}

.pre-wrap {
    white-space: pre-wrap;
}
.reduced-line-height {
    line-height: 1.2; /* 调整为较小的值，默认值通常是1.5 */
}

</style>
