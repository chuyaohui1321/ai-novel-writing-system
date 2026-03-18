import api from '../utils/api'

export const outlineApi = {
  generateFull(data) {
    return api.post('/outline/full', data)
  },
  read(projectId, outlineType = 'full') {
    return api.get('/outline/read', { params: { project_id: projectId, outline_type: outlineType } })
  },
  save(data) {
    return api.post('/outline/save', data)
  }
}
