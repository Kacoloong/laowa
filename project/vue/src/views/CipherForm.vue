<template>
    <el-container style="height: 100vh;">
        <el-header class="header">
            <div class="header-title">杂凑密码自动化设计与分析工具</div>
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
                        <el-menu-item index="2-1" @click="$router.push('/cipherForm')">Rebound分析</el-menu-item>
                        <el-menu-item index="2-2">差分碰撞</el-menu-item>
                        <el-menu-item index="2-3">中间相遇</el-menu-item>
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
                <div class="form-container">
                    <div class="upload-row">
                        <span class="upload-label">选择杂凑密码描述文件:</span>
                        <el-upload class="upload-demo" action="#" :auto-upload="false" :on-change="handleFileChange" drag>
                            <i class="el-icon-upload"></i>
                            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        </el-upload>
                        <el-button type="primary" @click="submitForm" :style="{ 'margin-left': '50px' }">提交</el-button>
                    </div>
                    <el-form label-width="300px" class="form-content">
                        <div class="form-row">
                            <el-form-item >
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法名称:</span>
                                </template>
                                <el-input v-model="cipherName" placeholder="请输入杂凑密码算法的名称" type="textarea"
                                    :style="{ width: cipherNameWidth + 'px', height: cipherNameHeight + 'px', resize: 'both', 'font-size': '20px' }"
                                    ></el-input>
                            </el-form-item>
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法状态表示:</span>
                                </template>
                                <el-input v-model="cipherState" placeholder="请输入杂凑密码算法的状态" type="textarea"
                                    :style="{ width: cipherStateWidth + 'px', height: cipherStateHeight + 'px', resize: 'both', 'font-size': '20px' }"
                                    ></el-input>
                            </el-form-item>
                        </div>
                        <div class="form-row">
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法移位向量:</span>
                                </template>
                                <el-input v-model="cipherShift" placeholder="请输入移位向量" type="textarea"
                                    :style="{ width: cipherShiftWidth + 'px', height: cipherShiftHeight + 'px', resize: 'both', 'font-size':'20px' }"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法线性变换规则:</span>
                                </template>
                                <el-input v-model="cipherMRMC" placeholder="请输入线性变换规则" type="textarea"
                                    :style="{ width: cipherMRMCWidth + 'px', height: cipherMRMCHeight + 'px', resize: 'both', 'font-size':'20px' }"></el-input>
                            </el-form-item>
                        </div>
                        <div class="form-row">
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法轮常数大小(字):</span>
                                </template>
                                <el-input v-model="cipherRCSize" placeholder="请输入轮常数大小" type="textarea"
                                    :style="{ width: cipherRCSizeWidth + 'px', height: cipherRCSizeHeight + 'px', resize: 'both', 'font-size':'20px' }"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">最后一轮是否包含线性变换:</span>
                                </template>
                                <el-input v-model="cipherLastRound" placeholder="请输入是否包含线性变换" type="textarea"
                                    :style="{ width: cipherLastRoundWidth + 'px', height: cipherLastRoundHeight + 'px', resize: 'both', 'font-size':'20px' }"></el-input>
                            </el-form-item>
                        </div>
                        <div class="form-row">
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法线性变换矩阵:</span>
                                </template>
                                <el-input v-model="cipherMDS" placeholder="请输入线性变换矩阵" type="textarea"
                                    :style="{ width: cipherMDSWidth + 'px', height: cipherMDSHeight + 'px', resize: 'both', 'font-size':'20px' }"></el-input>
                            </el-form-item>
                        </div>
                        <div class="form-row">
                            <el-form-item>
                                <template v-slot:label>
                                    <span style="font-size: 20px;">杂凑密码算法S盒:</span>
                                </template>
                                <el-input v-model="cipherSBox" placeholder="请输入S盒的值" type="textarea" :rows="8"
                                    :style="{ width: cipherSBoxWidth + 'px', height: cipherSBoxHeight + 'px', resize: 'both', 'font-size':'20px' }"></el-input>
                            </el-form-item>
                        </div>
                    </el-form>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    data() {
        return {
            cipherName: '',
            cipherState: '',
            cipherSBox: '',
            cipherMDS: '',
            cipherShift: '',
            cipherMRMC: '',
            cipherRCSize: '',
            cipherLastRound: '',
            result: null,
            cipherNameWidth: 200,
            cipherNameHeight: 50,
            cipherStateWidth: 200,
            cipherStateHeight: 50,
            cipherSBoxWidth: 720,
            cipherSBoxHeight: 50, // Increase the height for SBox
            cipherMDSWidth: 720,
            cipherMDSHeight: 50,
            cipherShiftWidth: 200,
            cipherShiftHeight: 50,
            cipherMRMCWidth: 200,
            cipherMRMCHeight: 50,
            cipherRCSizeWidth: 200,
            cipherRCSizeHeight: 50,
            cipherLastRoundWidth: 200,
            cipherLastRoundHeight: 50,
        };
    },
    methods: {
        async submitForm() {
            const response = await fetch('http://127.0.0.1:5000/submit-cipher', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cipherName: this.cipherName,
                    cipherState: this.cipherState,
                    cipherSBox: this.cipherSBox,
                    cipherMDS: this.cipherMDS,
                    cipherShift: this.cipherShift,
                    cipherMRMC: this.cipherMRMC,
                    cipherRCSize: this.cipherRCSize,
                    cipherLastRound: this.cipherLastRound,
                }),
            });
            const data = await response.json();
            this.result = data.result;
            this.$router.push('/rebound-analysis');
        },
        handleFileChange(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const content = e.target.result;
                this.parseFileContent(content);
            };
            reader.readAsText(file.raw);
        },
        parseFileContent(content) {
            const lines = content.split('\n');
            const cipherFeature = lines.map(line => line.split(':')[1].trim());

            if (cipherFeature.length >= 8) {
                this.cipherName = cipherFeature[0];
                this.cipherState = cipherFeature[1];
                this.cipherSBox = cipherFeature[2];
                this.cipherMDS = cipherFeature[3];
                this.cipherShift = cipherFeature[4];
                this.cipherMRMC = cipherFeature[5] === '0' ? '列混淆行移位' : '行混淆列移位';
                this.cipherLastRound = cipherFeature[6] === '0' ? '最后一轮不含线性变换' : '最后一轮包含线性变换';
                this.cipherRCSize = cipherFeature[7];
            }
        },
    },
};
</script>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-top: -150px; /* 或者将其设置为0，或者更小的正值 */
}

.upload-row {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    font-size: 20px;
}

.upload-label {
    margin-right: 50px;
}

.form-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* font-size: 24px; */
}

.form-row {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-bottom: 20px;
    
}


.form-row .el-form-item {
    flex: 1;
    margin-right: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
}
.custom-label .el-form-item__label {
  font-size: 24px; /* 设置你想要的字体大小 */
}
.el-form-lable {
  font-size: 24px;
}
.form-row .el-form-item:last-child {
    margin-right: 0;
}

.submit-row {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 20px;
}

.el-upload__text {
    color: #909399 !important;
    font-size: 20px !important;
}

.box-card {
    margin-top: 20px;
}

.el-input__inner {
    font-size: 24px !important;
}

.el-button--primary {
    font-size: 20px !important;
}

.el-form-item__label {
    font-size: 24px !important;
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

.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px;
    background-color: #fff;
}
</style>
