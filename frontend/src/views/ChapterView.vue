<template>
  <div class="chapter-view">
    <div class="view-header">
      <h3>章节列表</h3>
      <el-button type="primary" :icon="Plus" @click="showCreateDialog = true">新建章节</el-button>
    </div>

    <el-table :data="chapters" style="width: 100%">
      <el-table-column prop="name" label="章节名称" width="200" />
      <el-table-column prop="words" label="字数" width="120" />
      <el-table-column label="操作">
        <template #default="{ row, $index }">
          <el-button type="primary" size="small" @click="editChapter($index + 1)">编辑</el-button>
          <el-button type="success" size="small" @click="auditChapter($index + 1)">审计</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showCreateDialog" title="新建章节" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="章节号">
          <el-input-number v-model="form.chapter_number" :min="1" />
        </el-form-item>
        <el-form-item label="创作要求">
          <el-input v-model="form.context" type="textarea" :rows="4" placeholder="可选，填写本章的创作要求" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createChapter" :loading="creating">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { chapterApi } from '../api/chapter'
import { useAppStore } from '../store'

const router = useRouter()
const store = useAppStore()

const chapters = ref([])
const showCreateDialog = ref(false)
const creating = ref(false)
const form = ref({
  chapter_number: 1,
  context: ''
})

const createChapter = async () => {
  creating.value = true
  try {
    const res = await chapterApi.write({
      project_id: store.currentProject.id,
      chapter_number: form.value.chapter_number,
      context: form.value.context
    })
    if (res.data.code === 200) {
      ElMessage.success('章节创建成功')
      showCreateDialog.value = false
      chapters.value.push({
        name: `第${form.value.chapter_number}章`,
        words: 0
      })
    }
  } catch (error) {
    ElMessage.error('章节创建失败')
  } finally {
    creating.value = false
  }
}

const editChapter = (chapterNumber) => {
  store.setChapter(chapterNumber)
  router.push(`/chapter/${store.currentProject.id}/${chapterNumber}`)
}

const auditChapter = (chapterNumber) => {
  router.push(`/audit/${store.currentProject.id}`)
}

onMounted(() => {
  if (store.currentProject) {
    for (let i = 1; i <= (store.currentProject.chapter_count || 0); i++) {
      chapters.value.push({
        name: `第${i}章`,
        words: 0
      })
    }
  }
})
</script>

<style scoped>
.chapter-view {
  height: 100%;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
