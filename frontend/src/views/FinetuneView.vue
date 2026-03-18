<template>
  <div class="finetune-view">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>微调任务</span>
          </template>
          <el-menu :default-active="activeTask" @select="selectTask">
            <el-menu-item v-for="task in tasks" :key="task.id" :index="task.id">
              {{ task.base_model }}
              <el-tag size="small" :type="task.status === 'completed' ? 'success' : 'warning'" style="margin-left: 10px;">
                {{ task.status }}
              </el-tag>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>启动微调任务</span>
              <el-button type="primary" :icon="Plus" @click="showStartDialog = true">新建任务</el-button>
            </div>
          </template>
          
          <div v-if="currentTask" class="task-detail">
            <h4>任务进度</h4>
            <el-progress :percentage="progress" :status="progress === 100 ? 'success' : ''" />
            
            <h4 style="margin-top: 20px;">Loss 曲线</h4>
            <div class="loss-chart">
              <div v-for="(loss, i) in losses" :key="i" class="loss-bar" :style="{ height: (loss * 20) + 'px' }">
                {{ loss.toFixed(2) }}
              </div>
            </div>

            <h4 style="margin-top: 20px;">训练日志</h4>
            <el-input v-model="logContent" type="textarea" :rows="10" readonly />

            <div v-if="currentTask.status !== 'completed'" style="margin-top: 20px;">
              <el-button type="success" @click="deployModel">部署模型</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showStartDialog" title="启动微调任务" width="500px">
      <el-form :model="form" label-width="140px">
        <el-form-item label="基础模型">
          <el-input v-model="form.base_model" placeholder="例如: qwen3.5:7b" />
        </el-form-item>
        <el-form-item label="学习率">
          <el-input-number v-model="form.learning_rate" :min="1e-5" :max="1e-3" :step="1e-5" />
        </el-form-item>
        <el-form-item label="训练轮数">
          <el-input-number v-model="form.num_epochs" :min="1" :max="10" />
        </el-form-item>
        <el-form-item label="LoRA Rank">
          <el-input-number v-model="form.lora_rank" :min="4" :max="64" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showStartDialog = false">取消</el-button>
        <el-button type="primary" @click="startTask" :loading="starting">启动</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { finetuneApi } from '../api/finetune'

const tasks = ref([])
const activeTask = ref('')
const currentTask = ref(null)
const losses = ref([])
const logContent = ref('')
const showStartDialog = ref(false)
const starting = ref(false)
const form = ref({
  base_model: 'qwen3.5:7b',
  sample_files: [],
  learning_rate: 2e-4,
  num_epochs: 3,
  lora_rank: 8
})

const progress = computed(() => {
  if (!currentTask.value) return 0
  if (currentTask.value.status === 'completed') return 100
  return Math.min(90, losses.value.length * 10)
})

const loadTasks = async () => {
  try {
    const res = await finetuneApi.list()
    if (res.data.code === 200) {
      tasks.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  }
}

const selectTask = async (taskId) => {
  activeTask.value = taskId
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    currentTask.value = task
    try {
      const res = await finetuneApi.progress(taskId)
      if (res.data.code === 200) {
        losses.value = res.data.data.losses || []
        logContent.value = res.data.data.log || ''
      }
    } catch (error) {
      ElMessage.error('加载任务进度失败')
    }
  }
}

const startTask = async () => {
  starting.value = true
  try {
    const res = await finetuneApi.start(form.value)
    if (res.data.code === 200) {
      ElMessage.success('任务启动成功')
      showStartDialog.value = false
      loadTasks()
    }
  } catch (error) {
    ElMessage.error('任务启动失败')
  } finally {
    starting.value = false
  }
}

const deployModel = async () => {
  ElMessage.success('模型部署成功')
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.finetune-view {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-detail h4 {
  margin-bottom: 10px;
  color: #303133;
}

.loss-chart {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  height: 150px;
  padding: 20px 0;
}

.loss-bar {
  width: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 5px;
  font-size: 12px;
  border-radius: 4px 4px 0 0;
}
</style>
