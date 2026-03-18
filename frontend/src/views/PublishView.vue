<template>
  <div class="publish-view">
    <div class="view-header">
      <h3>发布管理</h3>
    </div>

    <el-card>
      <el-form :model="form" label-width="120px">
        <el-form-item label="选择章节">
          <el-checkbox-group v-model="selectedChapters">
            <el-checkbox v-for="n in chapterNumbers" :key="n" :label="n">第{{ n }}章</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="formatChapters">格式标准化</el-button>
          <el-button type="warning" @click="checkSensitive">敏感词检测</el-button>
          <el-button type="success" @click="exportChapters">批量导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px;" v-if="results.length > 0">
      <template #header>
        <span>处理结果</span>
      </template>
      <el-table :data="results" style="width: 100%">
        <el-table-column prop="chapter" label="章节" width="100" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'warning'">
              {{ row.status === 'success' ? '成功' : '警告' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="信息" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { publishApi } from '../api/publish'
import { useAppStore } from '../store'

const route = useRoute()
const store = useAppStore()

const form = ref({
  chapter_numbers: [],
  export_path: './export'
})
const selectedChapters = ref([])
const results = ref([])

const chapterNumbers = computed(() => {
  if (store.currentProject) {
    const count = store.currentProject.chapter_count || 10
    return Array.from({ length: count }, (_, i) => i + 1)
  }
  return [1, 2, 3, 4, 5]
})

const formatChapters = async () => {
  if (selectedChapters.value.length === 0) {
    ElMessage.warning('请选择要处理的章节')
    return
  }
  try {
    const res = await publishApi.format({
      project_id: route.params.projectId,
      chapter_numbers: selectedChapters.value
    })
    if (res.data.code === 200) {
      results.value = res.data.data.map(c => ({
        chapter: c.chapter,
        status: 'success',
        message: '格式标准化完成'
      }))
      ElMessage.success('格式标准化完成')
    }
  } catch (error) {
    ElMessage.error('格式标准化失败')
  }
}

const checkSensitive = async () => {
  if (selectedChapters.value.length === 0) {
    ElMessage.warning('请选择要检测的章节')
    return
  }
  try {
    const res = await publishApi.checkSensitive({
      project_id: route.params.projectId,
      chapter_numbers: selectedChapters.value
    })
    if (res.data.code === 200) {
      results.value = res.data.data.map(c => ({
        chapter: c.chapter,
        status: c.count === 0 ? 'success' : 'warning',
        message: c.count === 0 ? '无敏感词' : `发现 ${c.count} 个敏感词`
      }))
      ElMessage.success('敏感词检测完成')
    }
  } catch (error) {
    ElMessage.error('敏感词检测失败')
  }
}

const exportChapters = async () => {
  if (selectedChapters.value.length === 0) {
    ElMessage.warning('请选择要导出的章节')
    return
  }
  try {
    await publishApi.export({
      project_id: route.params.projectId,
      chapter_numbers: selectedChapters.value,
      export_path: './export'
    })
    ElMessage.success('导出完成')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}
</script>

<style scoped>
.publish-view {
  height: 100%;
}

.view-header {
  margin-bottom: 20px;
}
</style>
