<template>
  <div class="model-config-view">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>本地模型列表</span>
          </template>
          <el-table :data="models" style="width: 100%" @row-click="selectModel">
            <el-table-column prop="name" label="模型名称" />
            <el-table-column prop="size" label="大小" width="100" />
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card>
          <template #header>
            <span>模型配置</span>
          </template>
          <el-form :model="config" label-width="140px">
            <el-form-item label="配置方案名称">
              <el-input v-model="config.config_name" placeholder="请输入配置名称" />
            </el-form-item>
            <el-form-item label="选择模型">
              <el-select v-model="config.model_name" placeholder="请选择模型">
                <el-option v-for="model in models" :key="model.name" :label="model.name" :value="model.name" />
              </el-select>
            </el-form-item>
            <el-form-item label="Temperature">
              <el-slider v-model="config.temperature" :min="0" :max="2" :step="0.1" show-input />
            </el-form-item>
            <el-form-item label="Top P">
              <el-slider v-model="config.top_p" :min="0" :max="1" :step="0.1" show-input />
            </el-form-item>
            <el-form-item label="Max Tokens">
              <el-input-number v-model="config.max_tokens" :min="1024" :max="32768" :step="1024" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveConfig" :loading="saving">保存配置</el-button>
              <el-button type="success" @click="applyConfig">应用配置</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card style="margin-top: 20px;">
          <template #header>
            <span>已保存的配置方案</span>
          </template>
          <el-table :data="configList" style="width: 100%">
            <el-table-column prop="name" label="配置名称" />
            <el-table-column prop="model_name" label="模型" />
            <el-table-column prop="temperature" label="Temperature" width="120" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="loadConfig(row)">加载</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { modelApi } from '../api/model'

const models = ref([])
const configList = ref([])
const saving = ref(false)
const config = ref({
  config_name: '',
  model_name: '',
  temperature: 0.7,
  top_p: 0.9,
  max_tokens: 4096
})

const loadModels = async () => {
  try {
    const res = await modelApi.list()
    if (res.data.code === 200) {
      models.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('加载模型列表失败')
  }
}

const loadConfigList = async () => {
  try {
    const res = await modelApi.configList()
    if (res.data.code === 200) {
      configList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('加载配置列表失败')
  }
}

const selectModel = (row) => {
  config.value.model_name = row.name
}

const saveConfig = async () => {
  if (!config.value.config_name || !config.value.model_name) {
    ElMessage.warning('请填写完整信息')
    return
  }
  saving.value = true
  try {
    await modelApi.saveConfig(config.value)
    ElMessage.success('配置保存成功')
    loadConfigList()
  } catch (error) {
    ElMessage.error('配置保存失败')
  } finally {
    saving.value = false
  }
}

const loadConfig = (row) => {
  config.value = {
    config_name: row.name,
    model_name: row.model_name,
    temperature: row.temperature,
    top_p: row.top_p,
    max_tokens: row.max_tokens
  }
}

const applyConfig = async () => {
  ElMessage.success('配置已应用')
}

onMounted(() => {
  loadModels()
  loadConfigList()
})
</script>

<style scoped>
.model-config-view {
  height: 100%;
}
</style>
