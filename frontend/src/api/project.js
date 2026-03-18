import api from '../utils/api'

export const projectApi = {
  create(data) {
    return api.post('/project/create', data)
  },
  list() {
    return api.get('/project/list')
  },
  detail(projectId) {
    return api.get('/project/detail', { params: { project_id: projectId } })
  },
  delete(projectId) {
    return api.delete('/project/delete', { params: { project_id: projectId } })
  }
}
