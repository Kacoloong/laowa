<script setup>
import {ref} from "vue";

const hashLoading = ref(false)
const activeLoading = ref(false)
const generateStatus = ref(false)

const constant = ref(247)
const round = ref(14)
const column_1 = ref(3);
const column_2 = ref(2);
const column_3 = ref(1);
const column_4 = ref(2);
const mdsMatrix = ref([])


const lane = ref(null);
const sbox = ref(null);

const hashInput = ref('')
const hashValue = ref('')

const activeRound = ref(1)
const activeResult = ref(0)

const rows = 4;
const cols = 4;

for (let i = 0; i < rows; i++) {
  const row = [];
  for (let j = 0; j < cols; j++) {
    row.push(0); // Initialize each cell with a default value, e.g., 0
  }
  mdsMatrix.value.push(row);
}

function isFormValid() {
  return [
    // mdsMatrix.value.every(r => r.every(c => !!c)),
    constant.value,
    round.value,
    column_1.value,
    column_2.value,
    column_3.value,
    column_4.value,
  ].every(field => !!field);
}

function isHashInputValid() {
  return [
    hashInput
  ].every(field => !!field);
}

async function generateByteHash() {
  const response = await fetch('http://127.0.0.1:5000/api/hash_function/byte-generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'round': round.value,
      'constant': constant.value,
      'column_shift': [column_1.value, column_2.value, column_3.value, column_4.value],
      'mds': mdsMatrix.value
    })
  });
  const data = await response.json();
  if (data.code === 0) {
    const parameters = data.data;
    lane.value = parameters.lane
    sbox.value = parameters.sbox
    generateStatus.value = true
  } else {
    generateStatus.value = false
  }
}

async function fetchHash() {
  hashLoading.value = true
  const response = await fetch('http://127.0.0.1:5000/api/hash_function/calculate-hash', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({'type': 2, 'message': hashInput.value}),
  });
  const data = await response.json();
  if (data.code === 0) {
    hashValue.value = data.data.digesture
  }
  hashLoading.value = false
}

async function searchActiveSBox() {
  activeLoading.value = true
  const response = await fetch('http://127.0.0.1:5000/api/hash_function/byte/calculate-active-sbox', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({'round': activeRound.value}),
  });
  const data = await response.json();
  if (data.code === 0) {
    activeResult.value = data.data.count
  }
  activeLoading.value = false
}

</script>
<template>
  <el-row :gutter="30" justify="center">
    <el-col :span="20">
      <el-form class="compact-form" label-width="160px">
        <el-row :gutter="30" class="form-row">
          <el-col :span="12">
            <el-form-item>
              <template #label>
                <span style="color: red;">*</span>
                <span style="font-size: 14px;">轮常数:</span>
              </template>
              <el-input-number v-model="constant" :placeholder="14" :min="1" :max="255"
                               style="width: 100%; height: 60px; font-size: 13px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <template v-slot:label>
                <span style="color: red;">*</span>
                <span style="font-size: 14px;">轮数:</span>
              </template>
              <el-input-number v-model="round" :placeholder="20" :min="1" :max="30"
                               style="width: 100%; height: 60px; font-size: 13px;"/>
            </el-form-item>
          </el-col>
        </el-row>


        <el-row :gutter="30" class="form-row">
          <el-col :span="12">
            <el-form-item>
              <template v-slot:label>
                <span style="color: red;">*</span>
                <span style="font-size: 14px;">列位移:</span>
              </template>
              <el-select v-model="column_1" placeholder="请选择第一列位移:"
                         style="width: 100%; font-size: 14px; height: 36px;">
                <el-option v-for="c in 4" :key="c-1" :label="c-1" :value="c-1"></el-option>
              </el-select>
              <el-select v-model="column_2" placeholder="请选择第二列位移:"
                         style="width: 100%; font-size: 14px; height: 36px;">
                <el-option v-for="c in 4" :key="c-1" :label="c-1" :value="c-1"></el-option>
              </el-select>
              <el-select v-model="column_3" placeholder="请选择第三列位移:"
                         style="width: 100%; font-size: 14px; height: 36px;">
                <el-option v-for="c in 4" :key="c-1" :label="c-1" :value="c-1"></el-option>
              </el-select>
              <el-select v-model="column_4" placeholder="请选择第四列位移:"
                         style="width: 100%; font-size: 14px; height: 36px;">
                <el-option v-for="c in 4" :key="c-1" :label="c-1" :value="c-1"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>


        <el-row :gutter="30" class="form-row mds-container">
          <el-col :span="24">
            <el-form-item>
              <template v-slot:label>
                <span style="color: red;">*</span>
                <span style="font-size: 14px;">MDS矩阵:</span>
              </template>

              <div class="mds-matrix">
                <div v-for="row in 4" :key="row" class="mds-row" style="justify-content: flex-end;">
                  <el-input-number
                      v-for="col in 4"
                      :key="col"
                      v-model="mdsMatrix[row-1][col-1]"
                      :min="1"
                      :max="255"
                      :placeholder="1"
                      class="mds-cell"
                  />
                </div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-form-item class="button-group">
            <div class="btn-wrapper">
              <el-button :disabled="!isFormValid" class="action-btn" type="primary" @click="generateByteHash()">
                生成杂凑函数
              </el-button>
            </div>
          </el-form-item>
        </el-row>
      </el-form>
    </el-col>
  </el-row>

  <el-row v-if="generateStatus" class="status-message">
    <el-alert :closable="false" title="杂凑函数已生成" type="success"/>
  </el-row>
  <el-row v-if="generateStatus" :gutter="30" justify="center" style="margin-top: 30px;">
    <el-col :span="12">
      <el-card class="result-card">
        <h3>MDS矩阵</h3>
        <table class="compact-table">
          <tr v-for="(row, i) in mdsMatrix"
              :key="i">
            <td v-for="(cell, j) in row"
                :key="j"
                :class="i * 4 + j">
              {{ cell }}
            </td>
          </tr>
        </table>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card class="result-card">
        <h3>Lane变换常数</h3>
        <table class="compact-table">
          <tr v-for="(row, i) in lane"
              :key="i">
            <td v-for="(cell, j) in row"
                :key="j"
                :class="i * 4 + j">
              {{ cell }}
            </td>
          </tr>
        </table>
      </el-card>
    </el-col>
  </el-row>

  <el-row v-if="generateStatus" :gutter="30" justify="center" style="margin-top: 30px;">
    <el-col :span="24">
      <el-card class="result-card">
        <h3>S盒</h3>
        <table class="compact-table">
          <tr v-for="(row, i) in sbox"
              :key="i">
            <td v-for="(cell, j) in row"
                :key="j"
                :class="i * 4 + j">
              {{ cell }}
            </td>
          </tr>
        </table>
      </el-card>
    </el-col>
  </el-row>
  <el-row v-if="generateStatus" :gutter="30" justify="center" style="margin-top: 30px;">
    <el-col :span="12">
      <el-card class="function-module">
        <div class="module-title">杂凑函数输出测试</div>
        <el-form inline>
          <el-input
              v-model="hashInput"
              placeholder="输入明文"
              style="width: 300px; margin-right: 15px;"
          />
          <el-button
              :disabled="!isHashInputValid"
              :loading="hashLoading"
              type="primary"
              @click="fetchHash"
          >计算哈希值
          </el-button>
        </el-form>
        <div v-if="hashValue" class="result-box">
          <div class="result-label">哈希值：</div>
          <pre class="hash-output">{{ hashValue }}</pre>
        </div>
      </el-card>
    </el-col>
    <el-col :span="12">
      <!-- 活跃S盒搜索模块 -->
      <el-card class="function-module">
        <div class="module-title">活跃S盒搜索</div>
          <el-input-number style="width: 120px; margin-right: 15px;" v-model="activeRound" :min="1" :max="20" :placeholder="1" />
          <el-button
              :loading="activeLoading"
              type="primary"
              @click="searchActiveSBox"
          >开始搜索
          </el-button>
        <div v-if="activeResult" class="result-box">
          <div class="result-label">活跃S盒数量：</div>
          <div class="number-result">{{ activeResult }}</div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>


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
  margin-top: 20px;
}

.btn-wrapper {
  display: flex;
  gap: 150px;
}

.action-btn {
  font-size: 15px;
  padding: 12px 24px;
}

.mds-container {
  margin-top: 20px;
}

.mds-matrix {
  margin-left: 100px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  padding: 10px;
  background: #f8f9fa;
}

.mds-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.mds-cell {
  width: 110px;

  :deep(.el-input__inner) {
    text-align: center;
    font-family: monospace;
    font-size: 13px;
    padding: 0 5px;
  }
}

/* 高亮聚焦样式 */
:deep(.mds-cell.is-active) {
  .el-input__inner {
    border-color: #409EFF;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, .3);
  }
}

.function-module {
  margin-bottom: 25px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
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

.probability-result sup {
  font-size: 0.8em;
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

.result-card {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 15px;
  background: white;
  transition: box-shadow 0.3s;

  &:hover {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
