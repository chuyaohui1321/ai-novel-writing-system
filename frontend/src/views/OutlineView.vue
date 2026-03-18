<template>
  <div class="outline-view">
    <div class="view-header">
      <h3>大纲管理</h3>
      <div class="header-actions">
        <el-button :icon="Download" @click="loadOutline">加载大纲</el-button>
        <el-button type="primary" :icon="Plus" @click="showGenerateDialog = true">生成全卷大纲</el-button>
        <el-button type="success" :icon="Check" @click="saveOutline">保存大纲</el-button>
      </div>
    </div>

    <el-input
      v-model="outlineContent"
      type="textarea"
      :rows="30"
      placeholder="在此编辑大纲内容..."
    />

    <el-dialog v-model="showGenerateDialog" title="生成全卷大纲" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="核心创意">
          <el-input v-model="form.core_idea" type="textarea" :rows="3" placeholder="请输入小说的核心创意" />
        </el-form-item>
        <el-form-item label="分卷数量">
          <el-input-number v-model="form.volume_count" :min="1" :max="20" />
        </el-form-item>
        <el-form-item label="每卷章节数">
          <el-input-number v-model="form.chapters_per_volume" :min="5" :max="100" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showGenerateDialog = false">取消</el-button>
        <el-button type="primary" @click="generateOutline" :loading="generating">生成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Download, Check } from '@element-plus/icons-vue'
import { outlineApi } from '../api/outline'
import { useAppStore } from '../store'

const route = useRoute()
const store = useAppStore()

const outlineContent = ref('')
const showGenerateDialog = ref(false)
const generating = ref(false)
const form = ref({
  core_idea: '',
  volume_count: 5,
  chapters_per_volume: 20
})

const loadOutline = async () => {
  try {
    const res = await outlineApi.read(route.params.projectId)
    if (res.data.code === 200) {
      outlineContent.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('加载大纲失败')
  }
}

const saveOutline = async () => {
  try {
    await outlineApi.save({
      project_id: route.params.projectId,
      outline_type: 'full',
      content: outlineContent.value
    })
    ElMessage.success('大纲保存成功')
  } catch (error) {
    ElMessage.error('保存大纲失败')
  }
}

const generateOutline = async () => {
  if (!form.value.core_idea) {
    ElMessage.warning('请输入核心创意')
    return
  }
  generating.value = true
  try {
    const res = await outlineApi.generateFull({
      project_id: route.params.projectId,
      ...form.value
    })
    if (res.data.code === 200) {
      outlineContent.value = res.data.outline
      ElMessage.success('大纲生成成功')
      showGenerateDialog.value = false
    }
  } catch (error) {
    ElMessage.error('大纲生成失败')
  } finally {
    generating.value = false
  }
}

onMounted(() => {
  loadOutline()
})
</script>

<style scoped>
.outline-view {
  height: 100%;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
