import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/projects'
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/ProjectView.vue')
  },
  {
    path: '/workspace/:projectId',
    name: 'Workspace',
    component: () => import('../views/WorkspaceView.vue'),
    props: true
  },
  {
    path: '/outline/:projectId',
    name: 'Outline',
    component: () => import('../views/OutlineView.vue'),
    props: true
  },
  {
    path: '/chapter/:projectId/:chapterNumber',
    name: 'Chapter',
    component: () => import('../views/ChapterView.vue'),
    props: true
  },
  {
    path: '/audit/:projectId',
    name: 'Audit',
    component: () => import('../views/AuditView.vue'),
    props: true
  },
  {
    path: '/model-config',
    name: 'ModelConfig',
    component: () => import('../views/ModelConfigView.vue')
  },
  {
    path: '/finetune',
    name: 'Finetune',
    component: () => import('../views/FinetuneView.vue')
  },
  {
    path: '/publish/:projectId',
    name: 'Publish',
    component: () => import('../views/PublishView.vue'),
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
