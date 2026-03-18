import api from '../utils/api'

export const auditApi = {
  chapter(data) {
    return api.post('/audit/chapter', data)
  },
  global(data) {
    return api.post('/audit/global', data)
  },
  fix(data) {
    return api.post('/audit/fix', data)
  }
}
