<template>
  <div id="app">
    <el-container class="app-container">
      <el-header class="app-header">
        <div class="header-left">
          <el-icon class="logo-icon"><Document /></el-icon>
          <h1 class="app-title">AI长篇小说创作系统</h1>
        </div>
        <div class="header-right">
          <router-link to="/model-config">
            <el-button type="primary" :icon="Setting">模型配置</el-button>
          </router-link>
        </div>
      </el-header>
      <el-container class="main-container">
        <el-aside width="220px" class="app-aside">
          <el-menu
            :default-active="activeMenu"
            router
            class="aside-menu"
          >
            <el-menu-item index="/projects">
              <el-icon><Folder /></el-icon>
              <span>项目管理</span>
            </el-menu-item>
            <el-menu-item index="/model-config">
              <el-icon><Setting /></el-icon>
              <span>模型配置</span>
            </el-menu-item>
            <el-menu-item index="/finetune">
              <el-icon><MagicStick /></el-icon>
              <span>模型微调</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="app-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  height: 100vh;
}

.app-container {
  height: 100%;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-icon {
  font-size: 28px;
}

.app-title {
  font-size: 22px;
  font-weight: 600;
}

.main-container {
  height: calc(100vh - 60px);
}

.app-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.aside-menu {
  border: none;
  height: 100%;
}

.app-main {
  background-color: #fff;
  padding: 20px;
  overflow-y: auto;
}
</style>
