<script setup>
import SideBar from "@/components/SideBar.vue";
// import HeaderBar from "@/components/HeaderBar.vue";
</script>
<template>
  <el-header class="header">
      <div class="header-title">杂凑密码自动化设计与分析工具 - 杂凑密码输出测试</div>
  </el-header>
  <el-container>
    <SideBar />
    <el-main style="padding: 15px;">
      <el-row :gutter="30" justify="center">
        <el-col :span="20">
          <el-card class="function-module">
            <div class="module-title">杂凑函数调用</div>
            
            <!-- 测试类型选择 -->
            <div class="test-type-selector">
              <el-radio-group v-model="testType" @change="resetResults">
                <el-radio-button label="bit">比特杂凑测试</el-radio-button>
                <el-radio-button label="byte">字节杂凑测试</el-radio-button>
              </el-radio-group>
            </div>
            
            <!-- 输入区域 -->
            <el-form :model="form" label-width="120px" class="input-form">
              <el-form-item 
                label="测试消息：" 
                :rules="[{ required: true, message: '请输入测试消息' }]"
              >
                <el-input
                  v-model="form.message"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入要计算杂凑值的消息"
                  clearable
                />
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  @click="calculateHash"
                  :loading="loading"
                  :disabled="!form.message"
                >
                  {{ testType === 'bit' ? '计算比特杂凑值' : '计算字节杂凑值' }}
                </el-button>
              </el-form-item>
            </el-form>
            
            <!-- 结果展示 -->
            <div class="result-section" v-if="result || error">
              <div class="result-header">
                <span class="title">测试结果</span>
                <el-tag :type="result ? 'success' : 'danger'">
                  {{ result ? '成功' : '失败' }}
                </el-tag>
              </div>
              
              <div v-if="result" class="result-content">
                <div class="result-label">杂凑值：</div>
                <div class="hash-value">{{ result }}</div>
                <div class="result-meta">
                  <span>长度：{{ result.length * 4 }} 位 ({{ result.length }} 个十六进制字符)</span>
                </div>
              </div>
              
              <div v-if="error" class="error-content">
                <el-alert :title="error.title" type="error" :description="error.detail" show-icon />
                <div class="solution" v-if="error.solution">
                  <el-icon><InfoFilled /></el-icon>
                  <span>{{ error.solution }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import HeaderBar from "@/components/HeaderBar.vue";
import SideBar from "@/components/SideBar.vue";

export default {
  components: {
    HeaderBar,
    SideBar
  },
  data() {
    return {
      testType: 'bit',
      form: {
        message: ''
      },
      loading: false,
      result: '',
      error: null
    };
  },
  methods: {
    // 重置结果
    resetResults() {
      this.result = '';
      this.error = null;
    },
    
    // 计算杂凑值
    async calculateHash() {
      this.loading = true;
      this.result = '';
      this.error = null;
      
      try {
        const type = this.testType === 'bit' ? 1 : 2;
        const response = await fetch('http://127.0.0.1:5000/api/hash_function/calculate-hash', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: type,
            message: this.form.message
          })
        });
        
        const data = await response.json();
        
        if (data.code === 0) {
          this.result = this.testType === 'bit' 
            ? data.data.hash 
            : data.data.digest;
        } else {
          // 处理错误信息
          this.handleError(data.code);
        }
      } catch (error) {
        this.handleError(104, `请求失败: ${error.message}`);
      } finally {
        this.loading = false;
      }
    },
    
    // 统一错误处理
    handleError(code) {
      let title, detail, solution;
      
      switch(code) {
        case 103:
          title = "杂凑函数未生成";
          break;
          
        case 102:
          title = "请确保输入了要计算的测试消息";
          break;
          
        default:
          title = "系统内部错误";
      }
      
      this.error = { title, detail, solution };
    }
  }
};
</script>

<style scoped>
.function-module {
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.module-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2d3d;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eaeefb;
}

.test-type-selector {
  margin-bottom: 25px;
  padding: 10px 0;
}

.input-form {
  margin-top: 20px;
}

.result-section {
  margin-top: 30px;
  padding: 20px;
  border-radius: 6px;
  background: #f8fafc;
  border: 1px solid #e4ecfb;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #dcdfe6;
}

.result-header .title {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
}

.result-content {
  padding: 15px;
  background: #fff;
  border-radius: 4px;
  border: 1px solid #ebeef5;
}

.result-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.hash-value {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  word-break: break-all;
  line-height: 1.6;
}

.result-meta {
  margin-top: 12px;
  font-size: 13px;
  color: #909399;
  text-align: right;
}

.error-content {
  padding: 10px 0;
}

.solution {
  margin-top: 15px;
  padding: 10px 15px;
  background: #fef0f0;
  border-radius: 4px;
  color: #f56c6c;
  display: flex;
  align-items: center;
}

.solution i {
  margin-right: 8px;
}

:deep(.el-alert__title) {
  font-size: 15px !important;
}
</style>