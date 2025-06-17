<script setup>
import SideBar from "@/components/SideBar.vue";
// import HeaderBar from "@/components/HeaderBar.vue";
</script>
<template>
  <el-header class="header">
      <div class="header-title">杂凑密码自动化设计与分析工具 - 面向比特的设计</div>
  </el-header>
    <el-container>
        <SideBar/>
        <el-main style="padding: 15px;">
            <el-row :gutter="30" justify="center">
                <el-col :span="20">
                    <el-form label-width="160px" class="compact-form">
                        <el-row :gutter="30" class="form-row">
                            <el-col :span="12">
                                <el-form-item>
                                    <template #label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">状态大小:</span>
                                    </template>
                                    <el-input v-model="param_b" placeholder="请输入状态大小的比特数" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template #label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">状态的行数:</span>
                                    </template>
                                    <el-input v-model="param_m" placeholder="请输入状态所包含的行数" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        
                        <el-row :gutter="30" class="form-row">
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">输出摘要的长度:</span>
                                    </template>
                                    <el-input v-model="param_hlen" placeholder="请输入输出摘要的比特数" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">容量大小:</span>
                                    </template>
                                    <el-input v-model="param_c" placeholder="请输入容量的比特数" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="30" class="form-row">
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">轮数:</span>
                                    </template>
                                    <el-input v-model="param_r" placeholder="请输入轮数的取值" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">S盒的位宽:</span>
                                    </template>
                                    <el-select v-model="param_w" placeholder="请选择S盒的位宽" style="width: 100%; font-size: 14px; height: 36px;">
                                        <el-option label="4bit" value="4bit"></el-option>
                                        <el-option label="5bit" value="5bit"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="30" class="form-row sbox-container" v-if="param_w">
                            <el-col :span="24">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">S盒（16进制输入）:</span>
                                    </template>
                                
                                    <div class="sbox-matrix">
                                        <div class="sbox-row" v-for="row in 4" :key="row" style="justify-content: flex-end;">
                                            <div class="sbox-index">
                                                {{ ((row-1)*(param_w === '5bit' ? 8 : 4)).toString(16).toUpperCase() }}x
                                            </div>
                                            <el-input
                                                v-for="col in (param_w === '5bit' ? 8 : 4)"
                                                :key="col"
                                                v-model="sboxMatrix[(row-1)*(param_w === '5bit' ? 8 : 4) + (col-1)]"
                                                class="sbox-cell"
                                                :maxlength="param_w === '5bit' ? 2 : 1"
                                                :placeholder="param_w === '5bit' ? 'FF' : 'F'"
                                                @input="updateSBoxValue"
                                            />
                                        </div>
                                    </div>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-form-item class="button-group">
                            <div class="btn-wrapper">
                                <el-button type="primary" @click="generateBitHash()" :disabled="!isFormValid" class="action-btn">生成杂凑密码</el-button>
                                <el-button type="primary" @click="goHome()" class="action-btn">返回主页</el-button>
                            </div>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>

            <el-row :gutter="30" v-if="appear" justify="center" style="margin-top: 30px;">
                <el-col :span="20">
                    <!-- 生成状态提示 -->
                    <div v-if="generateStatus" class="status-message">
                        <el-alert title="杂凑函数已生成" type="success" :closable="false" />
                    </div>

                    <!-- 哈希计算模块 -->
                    <el-card class="function-module">
                        <div class="module-title">杂凑密码输出测试</div>
                        <el-form inline>
                            <el-input 
                                v-model="hashInput" 
                                placeholder="输入明文消息"
                                style="width: 300px; margin-right: 15px;"
                            />
                            <el-button 
                                type="primary" 
                                @click="handleHashRequest"
                                :loading="hashLoading"
                                :disabled="!isValid"
                            >计算杂凑值</el-button>
                        </el-form>
                        <div class="result-box" v-if="hashResult">
                            <div class="result-label">杂凑输出：</div>
                            <pre class="hash-output">{{ hashResult }}</pre>
                        </div>
                    </el-card>

                    <!-- 活跃S盒搜索模块 -->
                    <el-card class="function-module">
                        <div class="module-title">最小活跃S盒搜索</div>
                        <el-form inline>
                            <el-select 
                                v-model="activeRound" 
                                placeholder="选择轮数"
                                style="width: 120px; margin-right: 15px;"
                            >
                                <el-option 
                                    v-for="r in 6" 
                                    :key="r" 
                                    :label="`${r} 轮`" 
                                    :value="r"
                                />
                            </el-select>
                            <el-button 
                                type="primary" 
                                @click="searchActiveSBox"
                                :loading="activeLoading"
                            >开始搜索</el-button>
                        </el-form>
                        <div class="result-box" v-if="activeResult !== null">
                            <div class="result-label">最小活跃S盒数量：</div>
                            <div class="number-result">{{ activeResult }}</div>
                        </div>
                    </el-card>

                    <!-- 差分分析模块 -->
                    <el-card class="function-module">
                        <div class="module-title">差分概率分析</div>
                        <el-form inline>
                            <el-select 
                                v-model="diffRound" 
                                placeholder="选择轮数"
                                style="width: 120px; margin-right: 15px;"
                            >
                                <el-option 
                                    v-for="r in 4" 
                                    :key="r" 
                                    :label="`${r} 轮`" 
                                    :value="r"
                                />
                            </el-select>
                            <el-button 
                                type="primary" 
                                @click="searchDifferentialProbability"
                                :loading="diffLoading"
                            >开始分析</el-button>
                        </el-form>
                        <div class="result-box" v-if="diffResult !== null">
                            <div class="result-label">最大差分概率：</div>
                            <div class="probability-result">
                                2<sup>-{{ diffResult.exponent }}</sup> 
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script>
import { ElMessage } from 'element-plus';
export default {
  data() {
    return {
      // 表单数据定义
      param_b: '',
      param_c: '',
      param_hlen: '',
      param_m: '',
      param_r: '',
      param_w: '',
      sboxMatrix: Array(16).fill(''),
      generateStatus: false,
      hashInput: '',
      hashResult: '',
      hashLoading: false,
      activeRound: 1,
      activeResult: null,
      activeLoading: false,
      diffRound: 1,
      diffResult: null,
      diffLoading: false,
      appear: false,
    };
  },
  computed: {
      isFormValid() {
        return [
            this.param_b,    
            this.param_c,  
            this.param_hlen,    
            this.param_m,
            this.param_r,
            this.param_w, 
        ].every(field => !!field);
      },
      isValid() {
        return [
            this.hashInput
        ].every(field => !!field);
      }
    },
  watch: {
  param_w(newVal) {
    this.sboxMatrix = Array(newVal === '5bit' ? 32 : 16).fill('')
  }
  },
  methods: {
    goHome() {
      this.$router.push('/');
    },
    updateSBoxValue() {
    const padLength = this.param_w === '5bit' ? 2 : 1
    this.sbox_line_freq = this.sboxMatrix
      .map(v => v.padEnd(padLength, '0'))
      .join(' ')
      .toUpperCase()
    },
    rowSize(bitWidth) {
      return bitWidth === 4 ? 4 : 8;
    },
    chunkArray(arr, size) {
      return arr.reduce((acc, val, i) => {
        if (i % size === 0) acc.push([]);
        acc[acc.length - 1].push(val);
        return acc;
      }, []);
    },
    formatHex(value, bitWidth) {
      return value.toString(16)
        .toUpperCase()
        .padStart(Math.ceil(bitWidth/4), '0');
    },
    async generateBitHash() {
          const response = await fetch('http://127.0.0.1:5000/api/hash_function/bit-generate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                param_b: this.param_b,
                param_c: this.param_c,
                param_hlen: this.param_hlen,
                param_m: this.param_m,
                param_r: this.param_r,
                param_w: this.param_w,
                sboxMatrix: this.sboxMatrix
            }),
          });
          const results = await response.json();
          if (results.code === 0) {
            this.generateStatus = true
            this.appear = true
            this.hashResult = ''
            this.activeResult = null
            this.diffResult = null
            this.activeRound = 1
            this.diffRound = 1
            this.hashInput = ''
            ElMessage.success('杂凑密码生成成功')
            }
            else {
                this.generateStatus = false
                ElMessage.error('杂凑密码生成失败！')
            }
      },
      async handleHashRequest() {
      this.hashLoading = true
      try {
        const response = await fetch('http://127.0.0.1:5000/api/hash_function/calculate-hash', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 1, message: this.hashInput })
        })
        const temp = await response.json()
        const data = temp['data']
        this.hashResult = data.hash
      } catch (error) {
        ElMessage.error('哈希计算失败：' + error.message)
      } finally {
        this.hashLoading = false
      }
    },
    async searchActiveSBox() {
      this.activeLoading = true
      try {
        const response = await fetch('http://127.0.0.1:5000/api/hash_function/bit/calculate-active-sbox', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ rounds: this.activeRound })
        })
        const data = await response.json()
        this.activeResult = data['data'].count
      } catch (error) {
        ElMessage.error('搜索失败：' + error.message)
      } finally {
        this.activeLoading = false
      }
    },
    async searchDifferentialProbability() {
      this.diffLoading = true
      try {
        const response = await fetch('http://127.0.0.1:5000/api/hash_function/bit/search-differential-prob', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ rounds: this.diffRound })
        })
        const temp = await response.json()
        const data = temp['data']
        this.diffResult = {
          exponent: data.exponent,
        }
      } catch (error) {
        ElMessage.error('分析失败：' + error.message)
      } finally {
        this.diffLoading = false
      }
    }  
  }
};
</script>

<style scoped>
.compact-form {
    padding: 15px;
    background: #fff;
    border-radius: 6px;
}

.form-row {
    margin-bottom: 20px; 
}

.compact-item {
    padding: 10px;
    min-height: 90px;
    border: 1px solid #ebeef5;
}

.compact-item .el-form-item__label {
    line-height: 1.4;
    margin-bottom: 6px;
}

.el-select__caret {
    font-size: 14px;
}

.el-textarea__inner {
    min-height: 60px;
    padding: 6px 10px;
}

.button-group {
    display: flex;
    justify-content: flex-start; 
    padding-left: 170px;
    margin-top: 20px ;
}

.btn-wrapper {
    display: flex;
    gap: 150px;
}

.action-btn {
    font-size: 15px ;
    padding: 12px 24px ;
}

.centered-form .el-form-item {
    width: 100%;
}

.image-container {
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #dcdcdc;
    padding: 20px;
    min-height: 500px;
}

.placeholder {
    color: #909399;
}

.pre-wrap {
    white-space: pre-wrap;
}

.scrollable {
    max-height: 300px;
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

.sbox-container {
  margin-top: 20px;
}

.sbox-matrix {
  margin-left: 100px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  padding: 10px;
  background: #f8f9fa;
}

.sbox-header,
.sbox-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.sbox-index {
  width: 40px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #909399;
  background: #f0f2f5;
  border-radius: 4px;
}

.sbox-cell {
  width: 60px;
  
  :deep(.el-input__inner) {
    text-align: center;
    font-family: monospace;
    font-size: 13px;
    padding: 0 5px;
  }
}

.format-tips {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
  
  pre {
    margin: 5px 0;
    padding: 8px;
    background: #f8f9fa;
    border-radius: 4px;
    color: #67C23A;
  }
}

/* 高亮聚焦样式 */
:deep(.sbox-cell.is-active) {
  .el-input__inner {
    border-color: #409EFF;
    box-shadow: 0 0 0 2px rgba(64,158,255,.3);
  }
}

.function-module {
  margin-bottom: 25px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.module-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.result-box {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.result-label {
  color: #606266;
  font-size: 14px;
  margin-bottom: 8px;
}

.hash-output {
  font-family: monospace;
  font-size: 13px;
  word-wrap: break-word;
  white-space: pre-wrap;
  background: #fff;
  padding: 10px;
  border-radius: 4px;
}

.number-result {
  font-size: 24px;
  color: #409EFF;
  font-weight: 500;
}

.probability-result {
  font-size: 18px;
  color: #67C23A;
}
.probability-result sup {
  font-size: 0.8em;
}


</style>
