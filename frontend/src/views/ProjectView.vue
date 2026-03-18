<template>
  <div class="project-view">
    <div class="view-header">
      <h2>项目管理</h2>
      <el-button type="primary" :icon="Plus" @click="showCreateDialog = true">
        新建项目
      </el-button>
    </div>

    <div v-loading="loading" class="project-list">
      <el-empty v-if="!loading && projects.length === 0" description="暂无项目" />
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="project in projects" :key="project.id">
          <el-card class="project-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="project-title">{{ project.title }}</span>
                <el-tag :type="getGenreType(project.genre)">{{ project.genre }}</el-tag>
              </div>
            </template>
            <div class="project-info">
              <p><el-icon><Document /></el-icon> {{ project.chapter_count }} 章</p>
              <p><el-icon><Edit /></el-icon> {{ project.total_words }} 字</p>
              <p><el-icon><Clock /></el-icon> {{ project.create_time }}</p>
            </div>
            <div class="project-actions">
              <el-button type="primary" size="small" @click="openWorkspace(project)">
                进入工作区
              </el-button>
              <el-button type="danger" size="small" @click="deleteProject(project.id)">
                删除
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-dialog v-model="showCreateDialog" title="新建小说项目" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="小说名称">
          <el-input v-model="form.title" placeholder="请输入小说名称" />
        </el-form-item>
        <el-form-item label="小说题材">
          <el-select v-model="form.genre" placeholder="请选择题材">
            <el-option label="玄幻" value="xuanhuan" />
            <el-option label="都市" value="dushi" />
            <el-option label="科幻" value="kehuan" />
            <el-option label="言情" value="yanqing" />
            <el-option label="历史" value="lishi" />
          </el-select>
        </el-form-item>
        <el-form-item label="单章字数">
          <el-input-number v-model="form.chapter_words" :min="1000" :max="10000" :step="500" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createProject" :loading="creating">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Document, Edit, Clock } from '@element-plus/icons-vue'
import { projectApi } from '../api/project'
import { useAppStore } from '../store'

const router = useRouter()
const store = useAppStore()

const loading = ref(false)
const creating = ref(false)
const showCreateDialog = ref(false)
const projects = ref([])
const form = ref({
  title: '',
  genre: '',
  chapter_words: 3000
})

const getGenreType = (genre) => {
  const types = {
    xuanhuan: 'danger',
    dushi: 'success',
    kehuan: 'primary',
    yanqing: 'warning',
    lishi: 'info'
  }
  return types[genre] || 'info'
}

const loadProjects = async () => {
  loading.value = true
  try {
    const res = await projectApi.list()
    if (res.data.code === 200) {
      projects.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  } finally {
    loading.value = false
  }
}

const createProject = async () => {
  if (!form.value.title || !form.value.genre) {
    ElMessage.warning('请填写完整信息')
    return
  }
  creating.value = true
  try {
    const res = await projectApi.create(form.value)
    if (res.data.code === 200) {
      ElMessage.success('项目创建成功')
      showCreateDialog.value = false
      form.value = { title: '', genre: '', chapter_words: 3000 }
      loadProjects()
    }
  } catch (error) {
    ElMessage.error('项目创建失败')
  } finally {
    creating.value = false
  }
}

const openWorkspace = (project) => {
  store.setProject(project)
  router.push(`/workspace/${project.id}`)
}

const deleteProject = async (projectId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个项目吗？', '警告', {
      type: 'warning'
    })
    await projectApi.delete(projectId)
    ElMessage.success('项目删除成功')
    loadProjects()
  } catch {
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.project-view {
  height: 100%;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.view-header h2 {
  font-size: 24px;
  color: #303133;
}

.project-list {
  margin-top: 20px;
}

.project-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-title {
  font-weight: 600;
  font-size: 16px;
}

.project-info {
  margin: 15px 0;
}

.project-info p {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
  color: #606266;
}

.project-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}
</style>
