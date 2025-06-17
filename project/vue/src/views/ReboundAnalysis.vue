<template>
    <el-header class="header">
        <div class="header-title">杂凑密码自动化设计与分析工具 - Rebound分析</div>
    </el-header>
    <el-container>
        <SideBar/>
        <el-main style="padding: 10px;">
            <el-row :gutter="20" justify="center">
                <el-col :span="16">
                    <el-form label-width="150px" class="centered-form">
                        <el-row :gutter="20">
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 15px;">杂凑密码算法名称:</span>
                                    </template>
                                    <el-input v-model="cipher_name" placeholder="AES"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">杂凑密码算法行数:</span>
                                    </template>
                                    <el-input v-model="cipher_nrow" placeholder="请输入算法行数"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">杂凑密码算法列:</span>
                                    </template>
                                    <el-input v-model="cipher_ncolumn" placeholder="请输入算法列数"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="20">
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 15px;">杂凑密码算法移位向量:</span>
                                    </template>
                                    <el-input v-model="cipher_shift" placeholder="请输入移位向量"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">杂凑密码算法轮常数大小(字):</span>
                                    </template>
                                    <el-input v-model="cipher_rcsize" placeholder="请输入轮常数大小"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">杂凑密码算法线性变换规则:</span>
                                    </template>
                                    <el-select v-model="cipher_mrmc" placeholder="请选择线性变换规则">
                                        <el-option label="列混淆行移位" value="列混淆行移位"></el-option>
                                        <el-option label="行混淆列移位" value="行混淆列移位"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="20">
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 15px;">最后一轮是否包含线性变换:</span>
                                    </template>
                                    <el-select v-model="cipher_lastround" placeholder="请选择是否包含线性变换">
                                        <el-option label="最后一轮不含线性变换" value="最后一轮不含线性变换"></el-option>
                                        <el-option label="最后一轮包含线性变换" value="最后一轮包含线性变换"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">杂凑密码算法S盒:</span>
                                    </template>
                                    <el-input v-model="cipher_sbox" placeholder="请输入S盒的值"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">杂凑密码算法线性变换矩阵:</span>
                                    </template>
                                    <el-input v-model="cipher_mds" placeholder="请输入线性变换矩阵"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="20">
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 15px;">输入分析轮数:</span>
                                    </template>
                                    <el-input v-model="input_rounds" placeholder="请输入要分析的轮数" ></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">选择Inbound起始轮数:</span>
                                    </template>
                                    <el-input v-model="inbound_begin" placeholder="请输入Inbound的起始轮数" ></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">选择Inbound结束轮数:</span>
                                    </template>
                                    <el-input v-model="inbound_end" placeholder="请输入Inbound的结束轮数" ></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>


                        <el-row :gutter="20">
                            <el-col :span="8">
                                <el-form-item >
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">SubInbound个数:</span>
                                    </template>
                                    <el-input v-model="num_subinbound" placeholder="请输入SubInbound的个数"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item >
                                    <template v-slot:label>
                                        <span style="font-size: 15px;">SubInbound轮数分布:</span>
                                    </template>
                                    <el-input v-model="inbound_coverlist" placeholder="请输入SubInbound的轮数分布"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item >
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 15px;">生成解的个数:</span>
                                    </template>
                                    <el-input v-model="num_solution" placeholder="请输入生成解的个数"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-form-item class="button-group" :style="{ 'margin-top': '10px' }">
                            <el-button type="primary" @click="submitForm" :style="{ 'font-size': '15px', 'margin-right': '10px' }">单次Rebound分析</el-button>
                            <el-button type="primary" @click="startAnalysis" :style="{ 'font-size': '15px', 'margin-right': '10px' }">多次Rebound分析</el-button>
                            <el-button type="primary" @click="goHome" :style="{ 'font-size': '15px', 'margin-right': '10px' }">返回主页</el-button>
                            <!-- <el-button type="danger" @click="stopAnalysis" :style="{ 'font-size': '15px' }">停止分析</el-button> -->
                        </el-form-item>
                    </el-form>
                    <el-card class="box-card scrollable" ref="resultsContainer">
                        <h2>分析结果:</h2>
                         <div v-html="renderedResult" class="pre-wrap"></div>
                        <el-button v-if="results.length > 0" type="primary" @click="downloadResults">下载结果</el-button>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <div class="image-container">
                        <div>
                            <iframe :src="pdfSrc" width="530" height="730"></iframe>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script>

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import MarkdownIt from 'markdown-it';
import SideBar from "@/components/SideBar.vue";
// import HeaderBar from "@/components/HeaderBar.vue";

export default {
    //components: {SideBar, HeaderBar},
    components: {SideBar},
    setup() {
    const router = useRouter();
    const pdfSrc = ref('');
    const cipher_name= ref('AES');
        // const cipher_nrow= ref('');
    const cipher_nrow = ref(4); // 初始化为整数类型
        // const cipher_ncolumn= ref('');
    const cipher_ncolumn = ref(4); // 初始化为整数类型

    const cipher_sbox= ref([99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]);
    const cipher_mds= ref([2,3,1,1,1,2,3,1,1,1,2,3,3,1,1,2]);
    const cipher_mrmc= ref('');
    const cipher_rcsize= ref(16);
    const cipher_lastround= ref('');
    const cipher_shift= ref([0,1,2,3]);
    const input_rounds = ref(6);
    const inbound_begin = ref(2);
    const inbound_end = ref(3);
    const num_subinbound = ref(1);
    const inbound_coverlist = ref([2]);
    const num_solution = ref(1);
    const results = ref([]);
    const resultText = ref('');
    const renderedResult = ref('');
    const resultsContainer = ref(null);
    const md = new MarkdownIt();
    const controller = ref(null);
    let pollInterval = null;  // 用于保存定时器ID

    const submitForm = async () => {
        const response = await fetch('http://127.0.0.1:5000/api/hash_function/single-rebound', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cipher_name:cipher_name.value,
                cipher_nrow:cipher_nrow.value !== null && cipher_nrow.value !== undefined ? parseInt(cipher_nrow.value, 10) : null,
                cipher_ncolumn:cipher_ncolumn.value !== null && cipher_ncolumn.value !== undefined ? parseInt(cipher_ncolumn.value, 10) : null,
                cipher_sbox:cipher_sbox.value,
                cipher_mds:cipher_mds.value,
                cipher_mrmc:cipher_mrmc.value,
                cipher_rcsize:cipher_rcsize.value !== null && cipher_rcsize.value !== undefined ? parseInt(cipher_rcsize.value, 10) : null,
                cipher_lastround:cipher_lastround.value,
                cipher_shift:cipher_shift.value,
                input_rounds: input_rounds.value !== null && input_rounds.value !== undefined ? parseInt(input_rounds.value, 10) : null,
                inbound_begin: inbound_begin.value !== null && inbound_begin.value !== undefined ? parseInt(inbound_begin.value, 10) : null,
                inbound_end: inbound_end.value !== null && inbound_end.value !== undefined ? parseInt(inbound_end.value, 10) : null,
                num_subinbound: num_subinbound.value !== null && num_subinbound.value !== undefined ? parseInt(num_subinbound.value, 10) : null,
                inbound_coverlist: inbound_coverlist.value,
                num_solution: num_solution.value !== null && num_solution.value !== undefined ? parseInt(num_solution.value, 10) : null,
            }),
        });
        const data = await response.json();
        results.value.push(data);
        console.log('results.value:', results.value);

        if (data.code === 0) {
            // const resultText = ref('');
            resultText.value = '';
            resultText.value += `## Rebound 分析参数:\n`;
            resultText.value +=`**Rebound 分析轮数**: ${input_rounds.value}\n`;
            resultText.value += `**Rebound 分析中 Inbound 阶段**: 从第${inbound_begin.value}轮开始到第${inbound_end.value}轮结束\n`;
            resultText.value += `**Rebound 中 SubInbound 个数**: ${num_subinbound.value}\n`;
            resultText.value += `**Rebound 中 SubInbound 轮数分布**: ${inbound_coverlist.value}\n\n`;
            resultText.value += `## Rebound 分析结果:\n`;
            resultText.value += `**构造MILP模型时间**: ${data.data.c_model_time}s\n`;
            resultText.value += `**求解MILP模型时间**: ${data.data.s_model_time}s\n`;
            resultText.value += `**Rebound友好的截断差分路线**: ${data.data.solution}\n`;
            resultText.value += `**截断差分outbound概率乘上前后状态差分相等的概率**: ${data.data.pr}\n`;
            resultText.value += `**需要在Inbound阶段获得**: ${data.data.start_point}个起始点\n`;
            

            if (num_subinbound.value === 1) {
                resultText.value += `Inbound 阶段包含一轮, Inbound阶段求解一个起始点的平均时间复杂度为 1\n`;
                resultText.value += `**Rebound 分析的时间复杂度**: ${data.data.time}, **内存复杂度**: ${data.data.memory}\n`;
            } else {
                resultText.value += `**Rebound 分析的时间复杂度下界**: ${data.data.time}，还需要考虑连接多个Inbound阶段的时间复杂度\n`;
            }

            if (data.msg === 'success') {
                pdfSrc.value = `http://127.0.0.1:5000/api/hash_function/get-rebound-pdf?path=${encodeURIComponent(data.data.pdf_file)}`;
                // pdfSrc.value = `http://127.0.0.1:5000/${encodeURIComponent(data.result[2])}main.pdf`;
                console.log('pdfSrc.value:', pdfSrc.value);
            }
        }
        else{
            // resultText.value += `缺少参数`;
            // const resultText = ref('');
            resultText.value = '';
            resultText.value += `${data.msg}`;
        }
        
        
        updateRenderedResult();
        scrollToBottom();
    };

    const startAnalysis = async () => {
        results.value = []; // 清空之前的结果
        resultText.value = '';
        renderedResult.value = '';
        controller.value = new AbortController();

        const startResponse = await fetch('http://127.0.0.1:5000/api/hash_function/multiple-rebound', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cipher_name:cipher_name.value,
                cipher_nrow:cipher_nrow.value !== null && cipher_nrow.value !== undefined ? parseInt(cipher_nrow.value, 10) : null,
                cipher_ncolumn:cipher_ncolumn.value !== null && cipher_ncolumn.value !== undefined ? parseInt(cipher_ncolumn.value, 10) : null,
                cipher_sbox:cipher_sbox.value,
                cipher_mds:cipher_mds.value,
                cipher_mrmc:cipher_mrmc.value,
                cipher_rcsize:cipher_rcsize.value !== null && cipher_rcsize.value !== undefined ? parseInt(cipher_rcsize.value, 10) : null,
                cipher_lastround:cipher_lastround.value,
                cipher_shift:cipher_shift.value,
                input_rounds: input_rounds.value !== null && input_rounds.value !== undefined ? parseInt(input_rounds.value, 10) : null,
                num_solution: num_solution.value !== null && num_solution.value !== undefined ? parseInt(num_solution.value, 10) : null,
            }),
        });

        const startData = await startResponse.json();
        const taskId = startData.data.taskId;

        pollTaskStatus(taskId);
    };

    const pollTaskStatus = (taskId) => {
        const processedTaskIds = new Set(); // 记录已处理的任务ID
        pollInterval = setInterval(async () => {
            const statusResponse = await fetch(`http://127.0.0.1:5000/api/hash_function/check-rebound-status?taskId=${taskId}`, {
                signal: controller.value.signal,
            });
            const statusData = await statusResponse.json();
        
            if (statusData.data.status === 'completed' || statusData.data.status === 'failed') {
                clearInterval(pollInterval);
            }
        
            results.value = statusData.data.results;
            resultText.value = '';  // 清空现有的文本内容

            statusData.data.results.forEach((data) => {
                if (!data || !data.result) {
                    // console.error(`Missing analysis_result for result at index ${index}`);
                    return; // 跳过该项
                }
                resultText.value += `## Rebound 分析参数:\n`;
                resultText.value += `**Rebound 分析轮数**: ${input_rounds.value}\n`;
                resultText.value += `**Rebound 分析中 Inbound 阶段**: 从第${inbound_begin.value}轮开始到第${inbound_end.value}轮结束\n`;
                resultText.value += `**Rebound 中 SubInbound 个数**: ${num_subinbound.value}\n`;
                resultText.value += `**Rebound 中 SubInbound 轮数分布**: ${inbound_coverlist.value}\n\n`;
                resultText.value += `## Rebound 分析结果:\n`;
                resultText.value += `**构造MILP模型时间**: ${data.result.c_model_time}s\n`;
                resultText.value += `**求解MILP模型时间**: ${data.result.s_model_time}s\n`;
                resultText.value += `**Rebound友好的截断差分路线**: ${data.result.solution}\n`;
                resultText.value += `**截断差分outbound概率乘上前后状态差分相等的概率**: ${data.result.pr}\n`;
                resultText.value += `**需要在Inbound阶段获得**: ${data.result.start_point}个起始点\n`;
            
                if (num_subinbound.value === 1) {
                    resultText.value += `Inbound 阶段包含一轮, Inbound阶段求解一个起始点的平均时间复杂度为 1\n`;
                    resultText.value += `**Rebound 分析的时间复杂度**: ${data.result.time}, **内存复杂度**: ${data.result.memory}\n`;
                } else {
                    resultText.value += `**Rebound 分析的时间复杂度下界**: ${data.result.time}，还需要考虑连接多个Inbound阶段的时间复杂度\n`;
                }
                // resultText.value += `-` * 100;
                // resultText.value += '-'.repeat(100);

                resultText.value += '\n\n';
            });

            // 查找并更新 PDF 的路径
            const newPdfResult = statusData.data.results.find(r =>r.result.pdf_file && !processedTaskIds.has(r.id));
            if (newPdfResult) {
                pdfSrc.value = `http://127.0.0.1:5000/api/hash_function/get-rebound-pdf?path=${encodeURIComponent(newPdfResult.result.pdf_file)}`;
                console.log('PDF path updated:', pdfSrc.value);
                processedTaskIds.add(newPdfResult.id);
            }

            // resultText.value = statusData.results.map(r => r.result[1]).join('\n\n');
            // console.log('results:', results.value);
            // console.log('resultText:', resultText.value);

            // const newPdfResult = statusData.results.find(r => r.result[0] === true && r.result[2] && !processedTaskIds.has(r.id));
            // if (newPdfResult) {
            //     pdfSrc.value = `http://127.0.0.1:5000/pdf?path=${encodeURIComponent(newPdfResult.result[2])}`;
            //     console.log('PDF path updated:', pdfSrc.value);
            //     processedTaskIds.add(newPdfResult.id);
            // }
            updateRenderedResult();
            scrollToBottom();
        }, 2000); // 每2秒轮询一次
    };

    const stopAnalysis = () => {
        if (controller.value) {
            controller.value.abort(); // 中止fetch请求
        }
        if (pollInterval) {
            clearInterval(pollInterval); // 清除轮询定时器
        }
    };

        const updateRenderedResult = () => {
        console.log(resultText.value); // 检查内容是否正确
        renderedResult.value = md.render(resultText.value);
    };

    const scrollToBottom = () => {
        const container = resultsContainer.value;
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    };

    const downloadResults = () => {
        const element = document.createElement('a');
        const file = new Blob([resultText.value], { type: 'text/markdown' });
        element.href = URL.createObjectURL(file);
        element.download = 'analysis_results.md';
        document.body.appendChild(element);
        element.click();
    };

    onMounted(() => {
        resultsContainer.value = document.querySelector(".scrollable");
    });

    const goHome = () => {
        router.push('/');
    };

    return {
        pdfSrc,
        cipher_name,
        cipher_nrow,
        cipher_ncolumn,
        cipher_sbox,
        cipher_mds,
        cipher_mrmc,
        cipher_rcsize,
        cipher_lastround,
        cipher_shift,
        input_rounds,
        inbound_begin,
        inbound_end,
        num_subinbound,
        inbound_coverlist,
        num_solution,
        results,
        resultText,
        renderedResult,
        resultsContainer,
        submitForm,
        startAnalysis,
        stopAnalysis,
        goHome,
        downloadResults
    };
}

};
</script>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.centered-form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.button-group {
    display: flex;
    justify-content: center;
    gap: 50px;
    /* 按钮之间的间距 */
}

.centered-form .el-form-item {
    width: 100%;
}

.resizable-container {
    resize: both;
    overflow: auto;
    width: 200px;
    /* 默认宽度 */
    height: 50px;
    /* 自动高度 */
    min-width: 100px;
    /* 最小宽度 */
    min-height: 30px;
    /* 最小高度 */
}

.pdfobject-container {
    max-height: 800px;
    min-width: 300px;
    border: 1rem solid rgba(0, 0, 0, .1);
}

.image-container {
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #dcdcdc;
    padding: 20px;
    min-height: 500px;
}

.pdf-viewer {
    width: 100%;
    height: 400px;
    /* Adjust the height as needed */
    border: none;
}

.placeholder {
    color: #909399;
}

.box-card {
    margin-top: 30px;
    min-height: 400px;
    max-width: 900px;
}

.pre-wrap {
    white-space: pre-wrap;
}

.scrollable {
    max-height: 300px;
    /* Adjust this value as needed */
    overflow-y: scroll;
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
.sidebar {
    background-color: #f5f7fa;
    padding: 0px 0;
}
</style>
