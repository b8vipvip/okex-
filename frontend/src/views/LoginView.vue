<template>
  <div style="height:100vh;display:flex;align-items:center;justify-content:center;background:#f5f7fa">
    <el-card style="width:360px">
      <h3>管理员登录</h3>
      <el-form :model="form" @submit.prevent>
        <el-form-item><el-input v-model="form.username" placeholder="用户名"/></el-form-item>
        <el-form-item><el-input v-model="form.password" type="password" placeholder="密码"/></el-form-item>
        <el-button type="primary" style="width:100%" @click="onLogin">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>
<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi } from '../api'
import { useAuthStore } from '../stores/auth'
const router = useRouter()
const store = useAuthStore()
const form = reactive({ username: 'admin', password: 'admin123' })
const onLogin = async () => {
  const res = await loginApi(form)
  store.setToken(res.token)
  router.push('/dashboard')
}
</script>
