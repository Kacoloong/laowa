<script setup>
import {ref} from "vue";
import SideBar from "@/components/SideBar.vue";
// import HeaderBar from "@/components/HeaderBar.vue";
import {ElMessage} from 'element-plus';
import router from "@/router";

const xor_count = ref(6);
const loading = ref(false);
const mds_results = ref([]);
const appear = ref(false)
const matrix_size = ref(4)
const is_MDS = ref(true)
const column_shift_num = ref(1)
const lane_shift_num = ref(1)

async function fetchMDS() {
  const response = await fetch('http://127.0.0.1:5000/api/hash_function/mds-generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      'xor_count': xor_count.value,
      'is_MDS': is_MDS.value,
      'matrix_size': matrix_size.value,
      'column_shift_num': column_shift_num.value,
      'lane_shift_num': lane_shift_num.value
    })
  });
  loading.value = true;
  const data = await response.json();
  loading.value = false;
  if (data.code === 0) {
    mds_results.value = data.data['matrix'];
    appear.value = true
    ElMessage.success('MDS矩阵生成成功！');
  } else {
    ElMessage.error('MDS矩阵生成失败！');
  }
}

function goHome() {
  router.push('/');
}
</script>

<template>
  <el-header class="header">
      <div class="header-title">杂凑密码自动化设计与分析工具 - 面向字节的设计</div>
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
                    <span style="font-size: 14px;">MDS矩阵的异或和个数:</span>
                  </template>
                  <el-select v-model="xor_count" placeholder="请选择MDS矩阵的异或和个数"
                             style="width: 100%; font-size: 14px; height: 36px;">
                    <el-option label="6" value="6">6</el-option>
                    <el-option label="9" value="9">9</el-option>
                    <el-option label="12" value="12">12</el-option>
                    <el-option label="13" value="13">13</el-option>
                    <el-option label="14" value="14">14</el-option>
                    <el-option label="15" value="15">15</el-option>
                    <el-option label="16" value="16">16</el-option>
                    <el-option label="17" value="17">17</el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item>
                  <template v-slot:label>
                    <span style="color: red;">*</span>
                    <span style="font-size: 14px;">矩阵大小</span>
                  </template>
                  <el-input-number v-model="matrix_size" :min="4" :max="4"
                                   style="width: 100%; height: 60px; font-size: 13px;"/>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="30" class="form-row">
              <el-col :span="12">
                <el-form-item>
                  <template #label>
                    <span style="color: red;">*</span>
                    <span style="font-size: 14px;">是否MDS:</span>
                  </template>
                  <el-select v-model="is_MDS" placeholder="请选择矩阵是否满足MDS性质"
                             style="width: 100%; font-size: 14px; height: 36px;">
                    <el-option label="是" :value="true"></el-option>
                    <el-option label="否" :value="false"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="30" class="form-row">
              <el-col :span="12">
                <el-form-item>
                  <template v-slot:label>
                    <span style="color: red;">*</span>
                    <span style="font-size: 14px;">列移位数:</span>
                  </template>
                  <el-input-number v-model="column_shift_num" :min="0" :max="3" style="width: 100%; height: 60px; font-size: 13px;"/>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item>
                  <template v-slot:label>
                    <span style="color: red;">*</span>
                    <span style="font-size: 14px;">Lane变换:</span>
                  </template>
                  <el-input v-model="lane_shift_num" :min="0" :max="7" style="width: 100%; height: 60px; font-size: 13px;"/>
                </el-form-item>
              </el-col>
            </el-row>


            <el-form-item class="button-group">
              <div class="btn-wrapper">
                <el-button type="primary" @click="fetchMDS()" :disabled="loading" :loading="loading" class="action-btn">
                  生成MDS矩阵
                </el-button>
                <el-button type="primary" @click="goHome()" class="action-btn">返回主页</el-button>
              </div>
            </el-form-item>
          </el-form>

          <el-card v-if="appear">
            <div v-if="loading" class="loading-wrapper">
              <el-icon class="loading-icon" :size="30">
                <Loading/>
              </el-icon>
              <span class="loading-text">MDS矩阵生成中，请稍候...</span>
            </div>

            <div v-else-if="mds_results" class="dual-column">
              <div
                  v-for="(mds, index) in mds_results"
                  :key="index"
                  class="mds-card"
              >
                <h3>MDS矩阵生成结果 #{{ index + 1 }}</h3>
                <table class="compact-table">
                  <tr v-for="(row, i) in mds"
                      :key="i">
                    <td v-for="(cell, j) in row"
                        :key="j"
                        :class="i * 4 + j">
                      {{ cell }}
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

<style scoped>
.compact-item .el-form-item__label {
  line-height: 1.4;
  margin-bottom: 6px;
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

.function-module {
  margin-bottom: 25px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.probability-result sup {
  font-size: 0.8em;
}

.compact-form {
  padding: 15px;
  background: #fffff8;
  border-radius: 6px;
}

.form-row {
  margin-bottom: 20px;
}

.action-btn {
  font-size: 15px;
  padding: 12px 24px;
}

.dual-column {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 10px;
}

@media (max-width: 768px) {
  .dual-column {
    grid-template-columns: 1fr;
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

.mds-card {
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
