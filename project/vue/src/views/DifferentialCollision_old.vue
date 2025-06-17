<template>
    <el-header class="header">
        <div class="header-title">杂凑密码自动化设计与分析工具 - 差分碰撞攻击</div>
    </el-header>
    <el-container>
        <el-aside width="200px" class="sidebar">
            <el-menu>
                <el-menu-item index="1" @click="$router.push('/')">首页</el-menu-item>
                <el-sub-menu index="2">
                    <template #title>
                        <el-icon>
                            <location />
                        </el-icon>
                        <span>分析</span>
                    </template>
                    <el-menu-item index="2-1" @click="$router.push('/rebound-analysis')">Rebound分析</el-menu-item>
                    <el-menu-item index="2-2" @click="$router.push('/diff-collision')">差分碰撞</el-menu-item>
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
                                <el-form label-width="150px" class="centered-form">
                                    <el-row justify="center" :gutter="0">
                                        <el-col :span="8">
                                            <el-form-item label="轮数">
                                                <el-input v-model="rounds" placeholder="请输入轮数"></el-input>
                                                <span v-if="roundError" class="error-message">{{ roundError }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="状态大小">
                                                <el-input v-model="z_size" placeholder="请输入状态的大小"></el-input>
                                                <span v-if="zSizeError" class="error-message">{{ zSizeError }}</span>
                                            </el-form-item>
                                        </el-col>
                                    </el-row>

                                    <!-- 状态更新的6个循环移位值 -->
                                    <el-row justify="center" :gutter="20" style="margin-top: 10px;">
                                        <el-col :span="24">
                                            <h3 style="text-align: center; margin-bottom: 20px;">状态更新中的循环移位值</h3>
                                        </el-col>

                                        <!-- 第一行 -->
                                        <el-col :span="8">
                                            <el-form-item label="Status_i1 值:">
                                                <el-input v-model="status_i1" placeholder="请输入 Status_i1 值"></el-input>
                                                <span v-if="status_i1_error" class="error-message">{{ status_i1_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="Status_i2 值:">
                                                <el-input v-model="status_i2" placeholder="请输入 Status_i2 值"></el-input>
                                                <span v-if="status_i2_error" class="error-message">{{ status_i2_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="Status_i3 值:">
                                                <el-input v-model="status_i3" placeholder="请输入 Status_i3 值"></el-input>
                                                <span v-if="status_i3_error" class="error-message">{{ status_i3_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>

                                        <!-- 第二行 -->
                                        <el-col :span="8">
                                            <el-form-item label="Status_i4 值:">
                                                <el-input v-model="status_i4" placeholder="请输入 Status_i4 值"></el-input>
                                                <span v-if="status_i4_error" class="error-message">{{ status_i4_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="Status_i5 值:">
                                                <el-input v-model="status_i5" placeholder="请输入 Status_i5 值"></el-input>
                                                <span v-if="status_i5_error" class="error-message">{{ status_i5_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="Status_i6 值:">
                                                <el-input v-model="status_i6" placeholder="请输入 Status_i6 值"></el-input>
                                                <span v-if="status_i6_error" class="error-message">{{ status_i6_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                    </el-row>
                                    <!-- 消息字的6个循环移位值 -->
                                    <el-row justify="center" :gutter="20" style="margin-top: 10px;">
                                        <el-col :span="24">
                                            <h3 style="text-align: center; margin-bottom: 20px;">消息字中的循环移位值</h3>
                                        </el-col>

                                        <!-- 第一行 -->
                                        <el-col :span="8">
                                            <el-form-item label="msg_i1 值:">
                                                <el-input v-model="msg_i1" placeholder="请输入 msg_i1 值"></el-input>
                                                <span v-if="msg_i1_error" class="error-message">{{ msg_i1_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="msg_i2 值:">
                                                <el-input v-model="msg_i2" placeholder="请输入 msg_i2 值"></el-input>
                                                <span v-if="msg_i2_error" class="error-message">{{ msg_i2_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="msg_i3 值:">
                                                <el-input v-model="msg_i3" placeholder="请输入 msg_i3 值"></el-input>
                                                <span v-if="msg_i3_error" class="error-message">{{ msg_i3_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>

                                        <!-- 第二行 -->
                                        <el-col :span="8">
                                            <el-form-item label="msg_i4 值:">
                                                <el-input v-model="msg_i4" placeholder="请输入 msg_i4 值"></el-input>
                                                <span v-if="msg_i4_error" class="error-message">{{ msg_i4_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="msg_i5 值:">
                                                <el-input v-model="msg_i5" placeholder="请输入 msg_i5 值"></el-input>
                                                <span v-if="msg_i5_error" class="error-message">{{ msg_i5_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                        <el-col :span="8">
                                            <el-form-item label="msg_i6 值:">
                                                <el-input v-model="msg_i6" placeholder="请输入 msg_i6 值"></el-input>
                                                <span v-if="msg_i6_error" class="error-message">{{ msg_i6_error
                                                    }}</span>
                                            </el-form-item>
                                        </el-col>
                                    </el-row>



                                    <!-- 按钮组位于5x5数组下方居中 -->
                                    <el-row justify="center" style="margin-top: 10px;">
                                        <el-button type="primary" @click="analyze"
                                            style="margin: 0 10px;">开始分析</el-button>
                                        <el-button type="success" @click="generateChart"
                                            style="margin: 0 10px;">生成结果图</el-button>
                                        <el-button type="danger" @click="cancelAnalysis"
                                            style="margin: 0 10px;">取消分析</el-button>
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
        const rounds = ref(27);
        const z_size = ref(32);

        const pdfSrc = ref('');
        const renderedResult = ref('');
        const pdfFilePath = ref('');  // 将 pdfFilePath 定义为 ref
        const currentTaskId = ref(null); // 用于存储当前分析任务的 ID

        const roundError = ref('');
        const zSizeError = ref('');

        const msg_i1 = ref(7);
        const msg_i2 = ref(18);
        const msg_i3 = ref(3);
        const msg_i4 = ref(17);
        const msg_i5 = ref(19);
        const msg_i6 = ref(10);


        const status_i1 = ref(2);
        const status_i2 = ref(13);
        const status_i3 = ref(22);
        const status_i4 = ref(6);
        const status_i5 = ref(11);
        const status_i6 = ref(25);

        const msg_i1_error = ref('');
        const msg_i2_error = ref('');
        const msg_i3_error = ref('');
        const msg_i4_error = ref('');
        const msg_i5_error = ref('');
        const msg_i6_error = ref('');


        const status_i1_error = ref('');
        const status_i2_error = ref('');
        const status_i3_error = ref('');
        const status_i4_error = ref('');
        const status_i5_error = ref('');
        const status_i6_error = ref('');


        const analyze = async () => {
            // 每次分析前清空结果区域
            renderedResult.value = '';
            // 清空错误信息
            roundError.value = '';
            zSizeError.value = '';
            msg_i1_error.value = ''
            msg_i2_error.value = '';
            msg_i3_error.value = '';
            msg_i4_error.value = '';
            msg_i5_error.value = '';
            msg_i6_error.value = '';


            status_i1_error.value = '';
            status_i2_error.value = '';
            status_i3_error.value = '';
            status_i4_error.value = '';
            status_i5_error.value = '';
            status_i6_error.value = '';
            // 验证输入
            if (rounds.value < 27) {
                roundError.value = '轮数必须大于27';
                return;
            }
            if (![32, 64].includes(z_size.value)) {
                zSizeError.value = '状态的大小必须为32或64';
                return;
            }
            if (msg_i1.value > z_size.value) {
                msg_i1_error.value = '循环移位值必须小于 ${z_size.value}';
                return;
            }
            // if (msg_i2.value < z_size.value) {
            //     msg_i2_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (msg_i3.value < z_size.value) {
            //     msg_i3_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (msg_i4.value < z_size.value) {
            //     msg_i4_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (msg_i5.value < z_size.value) {
            //     msg_i5_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (msg_i6.value < z_size.value) {
            //     msg_i6_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (status_i1.value < z_size.value) {
            //     status_i1_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (status_i2.value < z_size.value) {
            //     status_i2_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (status_i3.value < z_size.value) {
            //     status_i3_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (status_i4.value < z_size.value) {
            //     status_i4_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (status_i5.value < z_size.value) {
            //     status_i5_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }
            // if (status_i6.value < z_size.value) {
            //     status_i6_error.value = '轮数必须大于 ${z_size.value}';
            //     return;
            // }



            try {
                currentTaskId.value = uuidv4(); // 生成唯一的 task_id
                const response = await axios.post('http://127.0.0.1:5000/diff-collision', {
                    method: 'POST',
                    rounds: parseInt(rounds.value, 10),  // 确保是整数
                    z_size: parseInt(z_size.value, 10),  // 转换 z_size 为整数
                    task_id: currentTaskId.value,// 将 task_id 发送到后端
                    msg_i1: parseInt(msg_i1.value, 10),  // 转换 msg_i1 为整数
                    msg_i2: parseInt(msg_i2.value, 10),  // 转换 msg_i2 为整数
                    msg_i3: parseInt(msg_i3.value, 10),  // 转换 msg_i3 为整数
                    msg_i4: parseInt(msg_i4.value, 10),  // 转换 msg_i4 为整数
                    msg_i5: parseInt(msg_i5.value, 10),  // 转换 msg_i5 为整数
                    msg_i6: parseInt(msg_i6.value, 10),  // 转换 msg_i6 为整数


                    status_i1: parseInt(status_i1.value, 10),  // 转换 status_i1 为整数
                    status_i2: parseInt(status_i2.value, 10),  // 转换 status_i2 为整数
                    status_i3: parseInt(status_i3.value, 10),  // 转换 status_i3 为整数
                    status_i4: parseInt(status_i4.value, 10),  // 转换 status_i4 为整数
                    status_i5: parseInt(status_i5.value, 10),  // 转换 status_i5 为整数
                    status_i6: parseInt(status_i6.value, 10),  // 转换 status_i6 为整数

                }, {
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
                    <p><strong>消息:</strong> ${data.message}</p>
                    <p><strong>Latex文件路径:</strong> ${data.tikz_file}</p>
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
            z_size,
            pdfSrc,
            renderedResult,
            analyze,
            generateChart,
            cancelAnalysis,

            msg_i1,
            msg_i2,
            msg_i3,
            msg_i4,
            msg_i5,
            msg_i6,


            status_i1,
            status_i2,
            status_i3,
            status_i4,
            status_i5,
            status_i6,


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
    line-height: 1.2;
    /* 调整为较小的值，默认值通常是1.5 */
}

.error-border .el-input {
    border-color: red;
}

.error-message {
    color: red;
    font-size: 12px;
}
</style>
