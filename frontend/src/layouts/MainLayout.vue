<template>
  <el-container class="app-shell">
    <el-aside class="app-aside" width="220px">
      <div class="brand">任务管理</div>
      <el-menu router :default-active="$route.path" class="nav-menu">
        <el-menu-item index="/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/import">批量导入</el-menu-item>
        <el-menu-item index="/tasks">任务列表</el-menu-item>
        <el-menu-item index="/prices">价格列表</el-menu-item>
        <el-menu-item index="/batches">批次列表</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container class="content-shell">
      <el-header class="app-header">
        <b>任务管理与执行回传系统</b>
        <el-button type="danger" link @click="logout">退出</el-button>
      </el-header>
      <el-main class="app-main"><router-view /></el-main>
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

<style scoped>
.app-shell { min-height: 100vh; background: #f3f6fb; }
.app-aside { background: #fff; border-right: 1px solid #e5e7eb; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04); }
.brand { height: 56px; display: flex; align-items: center; padding: 0 20px; font-weight: 800; color: #1d4ed8; letter-spacing: 1px; }
.nav-menu { border-right: 0; }
.content-shell { min-width: 0; }
.app-header { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.9); border-bottom: 1px solid #e5e7eb; backdrop-filter: blur(10px); }
.app-main { padding: 18px; overflow-x: hidden; }
@media (max-width: 768px) {
  .app-shell { display: block; }
  .app-aside { width: 100% !important; height: auto; border-right: 0; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 10; }
  .brand { height: 46px; justify-content: center; }
  .nav-menu { display: flex; overflow-x: auto; white-space: nowrap; }
  .nav-menu :deep(.el-menu-item) { flex: 0 0 auto; height: 44px; padding: 0 14px; }
  .app-header { height: auto; padding: 10px 12px; }
  .app-main { padding: 10px; }
}
</style>
