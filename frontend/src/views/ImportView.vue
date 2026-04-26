<template>
  <el-card>
    <el-form :model="form" label-width="100px">
      <el-form-item label="批次名称"><el-input v-model="form.batch_name"/></el-form-item>
      <el-form-item label="任务类型">
        <el-select v-model="form.task_type">
          <el-option label="充值" value="充值"/>
          <el-option label="查询价格" value="查询价格"/>
        </el-select>
      </el-form-item>
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
import { onMounted, reactive, ref, watch } from 'vue'
import { importTasksApi } from '../api'

const formatNowBatchName = () => {
  const now = new Date()
  const pad = (n) => `${n}`.padStart(2, '0')
  return `批量_${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`
}

const form = reactive({ batch_name: '', task_type: '充值', plan_type: 'month', sale_price: '0.00', text_content: '' })
const fileRef = ref(null)
const result = ref('')

watch(() => form.task_type, (taskType) => {
  if (taskType === '查询价格') {
    form.sale_price = '0.00'
    form.plan_type = 'month'
  }
})

onMounted(() => {
  form.batch_name = formatNowBatchName()
})

const onFile = (e) => { fileRef.value = e.target.files[0] }
const submit = async () => {
  const fd = new FormData()
  if (form.task_type === '查询价格') {
    form.sale_price = '0.00'
    form.plan_type = 'month'
  }
  Object.entries(form).forEach(([k, v]) => fd.append(k, v))
  if (fileRef.value) fd.append('file', fileRef.value)
  result.value = JSON.stringify(await importTasksApi(fd), null, 2)
}
</script>
