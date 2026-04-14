<template>
  <el-container style="height:100vh">
    <el-aside width="220px">
      <el-menu router :default-active="$route.path">
        <el-menu-item index="/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/import">批量导入</el-menu-item>
        <el-menu-item index="/tasks">任务列表</el-menu-item>
        <el-menu-item index="/batches">批次列表</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="display:flex;justify-content:space-between;align-items:center">
        <b>任务管理与执行回传系统</b>
        <el-button type="danger" link @click="logout">退出</el-button>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
const router = useRouter()
const store = useAuthStore()
const logout = () => {
  store.logout()
  router.push('/login')
}
</script>
