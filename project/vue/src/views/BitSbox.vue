<script setup>
import SideBar from "@/components/SideBar.vue";
//import HeaderBar from "@/components/HeaderBar.vue";
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
                                        <span style="font-size: 14px;">S盒的位宽:</span>
                                    </template>
                                    <el-select v-model="sbox_width" placeholder="请选择S盒的位宽" style="width: 100%; font-size: 14px; height: 36px;">
                                        <el-option label="4" value="4"></el-option>
                                        <el-option label="5" value="5"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template #label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">是否双射:</span>
                                    </template>
                                    <el-select v-model="sbox_bijection" placeholder="请选择S盒是否满足双射" style="width: 100%; font-size: 14px; height: 36px;">
                                        <el-option label="是" value="是"></el-option>
                                        <el-option label="否" value="否"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        
                        <el-row :gutter="30" class="form-row">
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">是否含不动点:</span>
                                    </template>
                                    <el-select v-model="sbox_fixed_point" placeholder="请选择S盒是否含有不动点" style="width: 100%; font-size: 14px; height: 36px;">
                                        <el-option label="是" value="是"></el-option>
                                        <el-option label="否" value="否"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">差分均匀度的上界:</span>
                                    </template>
                                    <el-input v-model="sbox_diff" placeholder="请输入差分均匀度的上界" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="30" class="form-row">
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">线性度的上界:</span>
                                    </template>
                                    <el-input v-model="sbox_line" placeholder="请输入线性度的上界" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">差分均匀度的频率的上界:</span>
                                    </template>
                                    <el-input v-model="sbox_diff_freq" placeholder="请输入差分均匀度的频率的上界" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row :gutter="30" class="form-row">
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">线性度的频率的上界:</span>
                                    </template>
                                    <el-input v-model="sbox_line_freq" placeholder="请输入线性度的频率的上界" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item>
                                    <template v-slot:label>
                                        <span style="color: red;">*</span>
                                        <span style="font-size: 14px;">BIBO模式的个数的上界:</span>
                                    </template>
                                    <el-input v-model="sbox_bibo" placeholder="请输入BIBO模式的个数的上界" type="textarea"
                                    style="width: 100%; height: 60px; font-size: 13px;"/>
                                </el-form-item>
                            </el-col>
                        </el-row>


                        <el-form-item class="button-group">
                            <div class="btn-wrapper">
                                <el-button type="primary" @click="generateSBox()" :disabled="!isFormValid || loading" :loading="loading" class="action-btn">生成S盒</el-button>
                                <el-button type="primary" @click="goHome()" class="action-btn">返回主页</el-button>
                            </div>
                        </el-form-item>
                    </el-form>

                    <el-card v-if="appear" class="result-container" >
                        <div v-if="error" class="error-wrapper">
                            <el-icon class="error-icon" :size="30" color="#F56C6C">
                                <CircleClose />
                            </el-icon>
                            <span class="error-text">S盒生成失败！</span>
                        </div>

                        <div v-if="loading" class="loading-wrapper">
                            <el-icon class="loading-icon" :size="30"><Loading /></el-icon>
                            <span class="loading-text">S盒生成中，请稍候...</span>
                        </div>

                        <div v-else-if="result" class="dual-column">
                            <div 
                            v-for="(sbox, index) in result" 
                            :key="index"
                            class="sbox-card"
                            >
                            <h3 class="sbox-title">S盒生成结果 #{{ index + 1 }}</h3>
                            
                            <table class="compact-table">
                                <tr v-for="(row, i) in chunkArray(sbox.data, rowSize(sbox.bitWidth))" 
                                    :key="i">
                                <td v-for="(cell, j) in row" 
                                    :key="j"
                                    :class="{ 'fixed-point': cell === i * rowSize(sbox.bitWidth) + j }">
                                    {{ formatHex(cell, sbox.bitWidth) }}
                                </td>
                                </tr>
                            </table>
                            </div>
                        </div>
                        </el-card>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script>
export default {
   data() {
      return {
          sbox_width: 4,
          sbox_bijection: '是',
          sbox_fixed_point: '是',
          sbox_diff: 4,
          sbox_line: 4,
          sbox_diff_freq: 8,
          sbox_line_freq: 8,
          sbox_bibo: 2,
          loading: false,
          appear: false,
          error: false,
          result: []
      };
  },
    computed: {
      isFormValid() {
        return [
            this.sbox_width,    
            this.sbox_bijection,  
            this.sbox_fixed_point,    
            this.sbox_diff,
            this.sbox_line,
            this.sbox_diff_freq, 
            this.sbox_line_freq,
            this.sbox_bibo
        ].every(field => !!field);
      }
    },
    methods: {
      goHome() {
        this.$router.push('/');
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
      async generateSBox() {
        this.appear = true;
        this.error = false;
        this.loading = true;
        try {
          const width = parseInt(this.sbox_width);
          const diff = parseInt(this.sbox_diff) || 0;
          const line = parseInt(this.sbox_line) || 0;
          const diffFreq = parseInt(this.sbox_diff_freq) || 0;
          const lineFreq = parseInt(this.sbox_line_freq) || 0;
          const bibo = parseInt(this.sbox_bibo) || 0;
          const response = await fetch('http://127.0.0.1:5000/api/hash_function/sbox-generate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              sbox_width: width,
              sbox_bijection: this.sbox_bijection,
              sbox_fixed_point: this.sbox_fixed_point,
              sbox_diff: diff,
              sbox_line: line,
              sbox_diff_freq: diffFreq,
              sbox_line_freq: lineFreq,
              sbox_bibo: bibo,
            }),
          });
          const temp = await response.json();
          const results = temp['data']
          this.result = results['data'].map(sbox => ({
              bitWidth: results['bitwidth'],
              data: sbox
          }))
        } catch (error) {
          console.error('请求失败:', error);
          this.error = true;
        } finally {
          this.loading = false;
        }
      },
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

.dual-column {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 10px;
}

.sbox-card {
    border: 1px solid #ebeef5;
    border-radius: 4px;
    padding: 15px;
    background: white;
    transition: box-shadow 0.3s;
  
    &:hover {
      box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }
}

.compact-table {
    border-collapse: collapse;
    width: 100%;
  
    tr:not(:last-child) td {
      border-bottom: 1px solid #e4e7ed;
    }
  
    td {
      padding: 8px 10px;
      text-align: center;
      font-family: monospace;
      position: relative;
    
      &:after {
        content: '';
        position: absolute;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 1px;
        height: 60%;
        background: #e4e7ed;
      }
    
      &:last-child:after {
        display: none;
      }
    }
}

.loading-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0;
  
    .loading-icon {
      margin-bottom: 15px;
      animation: rotating 2s linear infinite;
    }
  
    .loading-text {
      color: #909399;
      font-size: 0.95em;
    }
}

@keyframes rotating {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
    .dual-column {
        grid-template-columns: 1fr;
    }
  
  .compact-table td {
    padding: 6px 8px;
    font-size: 0.9em;
  }
}

.error-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0;
}

.error-icon {
    margin-bottom: 15px;
    animation: shake 0.6s ease-in-out;
}

.error-text {
    color: #F56C6C;
    font-size: 1.1em;
    margin-bottom: 15px;
}

.retry-btn {
    margin-top: 10px;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    75% { transform: translateX(8px); }
}
</style>
