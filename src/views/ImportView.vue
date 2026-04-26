<template>
  <el-card>
    <el-form :model="form" label-width="100px">
      <el-form-item label="批次名称"><el-input v-model="form.batch_name"/></el-form-item>
      <el-form-item label="套餐类型"><el-select v-model="form.plan_type"><el-option value="month"/><el-option value="season"/><el-option value="year"/></el-select></el-form-item>
      <el-form-item label="售价"><el-input v-model="form.sale_price"/></el-form-item>
      <el-form-item label="任务文本"><el-input v-model="form.text_content" type="textarea" :rows="10" placeholder="账号----备注"/></el-form-item>
      <el-form-item label="上传txt"><input type="file" accept=".txt" @change="onFile"/></el-form-item>
      <el-button type="primary" @click="submit">导入</el-button>
    </el-form>
    <pre v-if="result">{{ result }}</pre>
  </el-card>
</template>
<script setup>
import { reactive, ref } from 'vue'
import { importTasksApi } from '../api'
const form = reactive({ batch_name: '', plan_type: 'month', sale_price: '0.00', text_content: '' })
const fileRef = ref(null)
const result = ref('')
const onFile = (e) => { fileRef.value = e.target.files[0] }
const submit = async () => {
  const fd = new FormData()
  Object.entries(form).forEach(([k, v]) => fd.append(k, v))
  if (fileRef.value) fd.append('file', fileRef.value)
  result.value = JSON.stringify(await importTasksApi(fd), null, 2)
}
</script>
