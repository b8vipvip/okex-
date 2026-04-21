<template>
  <el-card>
    <el-form :inline="true" :model="q">
      <el-form-item label="关键词"><el-input v-model="q.keyword"/></el-form-item>
      <el-form-item label="状态"><el-select v-model="q.status" clearable><el-option v-for="s in statuses" :key="s" :label="s" :value="s"/></el-select></el-form-item>
      <el-form-item label="批次ID"><el-input v-model="q.batch_id"/></el-form-item>
      <el-button @click="load">搜索</el-button>
      <el-button @click="exportCsv">导出CSV</el-button>
    </el-form>
    <el-table :data="items" stripe>
      <el-table-column prop="task_no" label="任务编号" width="180"/>
      <el-table-column prop="account_identifier" label="账号"/>
      <el-table-column prop="account_remark" label="备注"/>
      <el-table-column prop="plan_type" label="套餐"/>
      <el-table-column label="状态">
        <template #default="{row}">
          {{ displayStatus(row) }}
        </template>
      </el-table-column>
      <el-table-column prop="progress_updated_at" label="状态更新时间" width="170"/>
      <el-table-column prop="sale_price" label="售价"/>
      <el-table-column prop="recharge_cost" label="成本"/>
      <el-table-column prop="profit" label="利润"/>
      <el-table-column prop="kugou_id" label="kugou_id"/>
      <el-table-column prop="worker_id" label="worker_id"/>
      <el-table-column prop="uploaded_at" label="上传时间" width="170"/>
      <el-table-column prop="started_at" label="开始时间" width="170"/>
      <el-table-column prop="finished_at" label="完成时间" width="170"/>
      <el-table-column prop="fail_reason" label="失败原因" width="180"/>
      <el-table-column label="操作"><template #default="{row}"><el-button link type="primary" @click="go(row.id)">详情</el-button></template></el-table-column>
    </el-table>
    <el-pagination background layout="prev, pager, next" :total="total" v-model:current-page="q.page" v-model:page-size="q.page_size" @current-change="load"/>
  </el-card>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { listTasksApi } from '../api'
const router = useRouter()
const statuses = ['pending','queued','claimed','processing','success','failed','cancelled']
const q = reactive({ page: 1, page_size: 20, keyword: '', status: '', batch_id: '' })
const items = ref([])
const total = ref(0)
const displayStatus = (task) => task.progress_status || task.status_text || task.status
const load = async () => {
  const data = await listTasksApi(q)
  items.value = data.items
  total.value = data.total
}
const go = (id) => router.push(`/tasks/${id}`)
const exportCsv = () => {
  const header = Object.keys(items.value[0] || {}).join(',')
  const rows = items.value.map((r) => Object.values(r).join(','))
  const csv = [header, ...rows].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `tasks_${Date.now()}.csv`
  a.click()
}
onMounted(load)
</script>
