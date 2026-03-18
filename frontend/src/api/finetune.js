import api from '../utils/api'

export const finetuneApi = {
  start(data) {
    return api.post('/finetune/start', data)
  },
  progress(taskId) {
    return api.get('/finetune/progress', { params: { task_id: taskId } })
  },
  deploy(data) {
    return api.post('/finetune/deploy', data)
  },
  list() {
    return api.get('/finetune/list')
  }
}
