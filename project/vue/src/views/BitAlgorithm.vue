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
                                        <el-option label="4" value="4"></el-option>
                                        <el-option label="5" value="5"></el-option>
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
                                                {{ ((row-1)*(param_w === '5' ? 8 : 4)).toString(16).toUpperCase() }}x
                                            </div>
                                            <el-input
                                                v-for="col in (param_w === '5' ? 8 : 4)"
                                                :key="col"
                                                v-model="sboxMatrix[(row-1)*(param_w === '5' ? 8 : 4) + (col-1)]"
                                                class="sbox-cell"
                                                :maxlength="param_w === '5' ? 2 : 1"
                                                :placeholder="param_w === '5' ? 'FF' : 'F'"
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
        </el-main>
    </el-container>
</template>

<script>
import { ElMessage } from 'element-plus';
export default {
  data() {
    return {
      // 表单数据定义
      param_b: 1500,
      param_c: 1024,
      param_hlen: 512,
      param_m: 24,
      param_r: 14,
      param_w: 4,
      sboxMatrix: ['3','C','8','5','D','A','1','6','9','F','E','0','7','4','2','B'],
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
      }
    },
  watch: {
  param_w(newVal) {
    this.sboxMatrix = Array(newVal === '5' ? 32 : 16).fill('')
  }
  },
  methods: {
    goHome() {
      this.$router.push('/');
    },
    updateSBoxValue() {
    const padLength = this.param_w === '5' ? 2 : 1
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
          const b = parseInt(this.param_b) || 0;
          const c = parseInt(this.param_c) || 0;
          const hlen = parseInt(this.param_hlen) || 0;
          const m =parseInt(this.param_m) || 0;
          const r = parseInt(this.param_r) || 0;
          const w = parseInt(this.param_w) || 0;
          const sboxMatrix = this.sboxMatrix.map(hex => {
            const num = parseInt(hex, 16);
            return isNaN(num) ? 0 : num;
          })
          const response = await fetch('http://127.0.0.1:5000/api/hash_function/bit-generate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                param_b: b,
                param_c: c,
                param_hlen: hlen,
                param_m: m,
                param_r: r,
                param_w: w,
                sboxMatrix: sboxMatrix
            }),
          });
          const results = await response.json();
          if (results.code === 0) {
            this.generateStatus = true
            ElMessage.success('杂凑密码生成成功')
            }
            else {
                this.generateStatus = false
                ElMessage.error('杂凑密码生成失败！')
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

/* 高亮聚焦样式 */
:deep(.sbox-cell.is-active) {
  .el-input__inner {
    border-color: #409EFF;
    box-shadow: 0 0 0 2px rgba(64,158,255,.3);
  }
}
</style>
