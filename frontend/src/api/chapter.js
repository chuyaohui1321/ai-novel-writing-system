import api from '../utils/api'

export const chapterApi = {
  write(data) {
    return api.post('/chapter/write', data)
  },
  read(projectId, chapterNumber, contentType = '正文') {
    return api.get('/chapter/read', { params: { project_id: projectId, chapter_number: chapterNumber, content_type: contentType } })
  },
  save(data) {
    return api.post('/chapter/save', data)
  },
  rewrite(data) {
    return api.post('/chapter/rewrite', data)
  }
}
