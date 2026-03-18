import api from '../utils/api'

export const modelApi = {
  list() {
    return api.get('/models/list')
  },
  configList() {
    return api.get('/models/config/list')
  },
  saveConfig(data) {
    return api.post('/models/config/save', data)
  },
  applyConfig(data) {
    return api.post('/models/config/apply', data)
  }
}
