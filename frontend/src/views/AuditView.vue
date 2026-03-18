<template>
  <div class="audit-view">
    <div class="view-header">
      <h3>审计校验</h3>
      <div class="header-actions">
        <el-button type="primary" :icon="Search" @click="auditChapter">审计单章</el-button>
        <el-button type="warning" :icon="DocumentChecked" @click="globalAudit">全局审计</el-button>
      </div>
    </div>

    <el-card v-if="auditReport">
      <template #header>
        <span>审计报告</span>
      </template>
      <div class="audit-content" v-html="formatReport(auditReport)"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, DocumentChecked } from '@element-plus/icons-vue'
import { auditApi } from '../api/audit'
import { useAppStore } from '../store'

const route = useRoute()
const store = useAppStore()

const auditReport = ref('')

const formatReport = (report) => {
  return report.replace(/\n/g, '<br>')
}

const auditChapter = async () => {
  try {
    const res = await auditApi.chapter({
      project_id: route.params.projectId,
      chapter_number: store.currentChapter
    })
    if (res.data.code === 200) {
      auditReport.value = res.data.audit_report
      ElMessage.success('审计完成')
    }
  } catch (error) {
    ElMessage.error('审计失败')
  }
}

const globalAudit = async () => {
  try {
    const res = await auditApi.global({
      project_id: route.params.projectId
    })
    if (res.data.code === 200) {
      auditReport.value = res.data.audit_report
      ElMessage.success('全局审计完成')
    }
  } catch (error) {
    ElMessage.error('全局审计失败')
  }
}
</script>

<style scoped>
.audit-view {
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

.audit-content {
  white-space: pre-wrap;
  line-height: 1.8;
}
</style>
