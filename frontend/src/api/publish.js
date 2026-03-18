import api from '../utils/api'

export const publishApi = {
  format(data) {
    return api.post('/publish/format', data)
  },
  checkSensitive(data) {
    return api.post('/publish/check_sensitive', data)
  },
  export(data) {
    return api.post('/publish/export', data)
  }
}
