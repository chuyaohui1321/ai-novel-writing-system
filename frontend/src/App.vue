<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>AI长篇小说创作系统</h1>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu default-active="1">
            <el-menu-item index="1">项目管理</el-menu-item>
            <el-menu-item index="2">大纲编辑</el-menu-item>
            <el-menu-item index="3">章节创作</el-menu-item>
            <el-menu-item index="4">审计校验</el-menu-item>
            <el-menu-item index="5">模型配置</el-menu-item>
            <el-menu-item index="6">微调管理</el-menu-item>
            <el-menu-item index="7">发布管理</el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <el-card>
            <template #header>
              <span>欢迎使用 AI 长篇小说创作系统</span>
            </template>
            <p>基于 InkOS Agent 的本地化 AI 创作工具</p>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
</script>

<style>
#app {
  height: 100vh;
}
.el-container {
  height: 100%;
}
.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
}
.el-aside {
  background-color: #f5f7fa;
}
</style>
