<template>
  <div class="workspace-view">
    <div class="view-header">
      <el-button :icon="ArrowLeft" @click="router.push('/projects')">返回</el-button>
      <h2 v-if="project">{{ project.project_info?.title }}</h2>
    </div>

    <el-row :gutter="20" class="workspace-content">
      <el-col :span="6">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>项目导航</span>
            </div>
          </template>
          <el-menu :default-active="activeSection" @select="handleSelect">
            <el-menu-item index="outline">
              <el-icon><Document /></el-icon>
              <span>大纲管理</span>
            </el-menu-item>
            <el-menu-item index="chapters">
              <el-icon><Files /></el-icon>
              <span>章节列表</span>
            </el-menu-item>
            <el-menu-item index="audit">
              <el-icon><CircleCheck /></el-icon>
              <span>审计校验</span>
            </el-menu-item>
            <el-menu-item index="publish">
              <el-icon><Upload /></el-icon>
              <span>发布管理</span>
            </el-menu-item>
          </el-menu>
        </el-card>

        <el-card class="section-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>项目统计</span>
            </div>
          </template>
          <div v-if="project" class="stats">
            <p>章节数: {{ project.chapter_count }}</p>
            <p>总字数: {{ project.total_words }}</p>
          </div>
        </el-card>
      </el-col>

      <el-col :span="18">
        <router-view />
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Document, Files, CircleCheck, Upload } from '@element-plus/icons-vue'
import { projectApi } from '../api/project'
import { useAppStore } from '../store'

const router = useRouter()
const route = useRoute()
const store = useAppStore()

const project = ref(null)
const activeSection = ref('chapters')

const loadProject = async () => {
  try {
    const res = await projectApi.detail(route.params.projectId)
    if (res.data.code === 200) {
      project.value = res.data.data
      store.setProject(res.data.data.project_info)
    }
  } catch (error) {
    ElMessage.error('加载项目失败')
  }
}

const handleSelect = (index) => {
  activeSection.value = index
  if (index === 'outline') {
    router.push(`/outline/${route.params.projectId}`)
  } else if (index === 'chapters') {
    router.push(`/workspace/${route.params.projectId}`)
  } else if (index === 'audit') {
    router.push(`/audit/${route.params.projectId}`)
  } else if (index === 'publish') {
    router.push(`/publish/${route.params.projectId}`)
  }
}

onMounted(() => {
  loadProject()
})
</script>

<style scoped>
.workspace-view {
  height: 100%;
}

.view-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.view-header h2 {
  font-size: 24px;
  color: #303133;
}

.workspace-content {
  height: calc(100% - 70px);
}

.section-card {
  height: fit-content;
}

.card-header {
  font-weight: 600;
}

.stats {
  color: #606266;
}

.stats p {
  margin: 10px 0;
}
</style>
