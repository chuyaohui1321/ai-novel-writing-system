import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentProject = ref(null)
  const currentChapter = ref(1)

  function setProject(project) {
    currentProject.value = project
  }

  function setChapter(chapterNumber) {
    currentChapter.value = chapterNumber
  }

  return {
    currentProject,
    currentChapter,
    setProject,
    setChapter
  }
})
