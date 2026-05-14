<template>
  <el-card class="page-card price-page" shadow="never">
    <template #header>
      <div class="page-header">
        <div>
          <div class="page-title">账号价格记录</div>
          <div class="page-subtitle">展示充值和查询价格任务回传的价格信息</div>
        </div>
        <el-button @click="load">刷新</el-button>
      </div>
    </template>

    <el-form :inline="true" :model="q" class="toolbar-form">
      <el-form-item label="关键词"><el-input v-model="q.keyword" clearable placeholder="任务编号/账号/备注/kugou_id"/></el-form-item>
      <el-form-item label="任务类型">
        <el-select v-model="q.task_type" clearable placeholder="全部类型">
          <el-option label="充值" value="充值"/>
          <el-option label="查询价格" value="查询价格"/>
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="q.status" clearable placeholder="全部状态">
          <el-option v-for="s in statusOptions" :key="s.value" :label="s.label" :value="s.value"/>
        </el-select>
      </el-form-item>
      <el-form-item class="toolbar-actions">
        <el-button type="primary" @click="load">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="items" stripe row-key="task_no" class="responsive-table">
      <el-table-column prop="task_no" label="任务编号" width="200"/>
      <el-table-column prop="task_type" label="任务类型" width="110"/>
      <el-table-column label="状态" width="100">
        <template #default="{row}">{{ statusText(row.status) }}</template>
      </el-table-column>
      <el-table-column prop="account_identifier" label="账号" width="180"/>
      <el-table-column prop="account_remark" label="密码" width="160"/>
      <el-table-column prop="app_month_price" label="APP月卡"/>
      <el-table-column prop="app_season_price" label="APP季卡"/>
      <el-table-column prop="app_year_price" label="APP年卡"/>
      <el-table-column prop="web_month_price" label="WEB月卡"/>
      <el-table-column prop="web_season_price" label="WEB季卡"/>
      <el-table-column prop="web_year_price" label="WEB年卡"/>
      <el-table-column prop="pc_month_price" label="PC月卡"/>
      <el-table-column prop="pc_season_price" label="PC季卡"/>
      <el-table-column prop="pc_year_price" label="PC年卡"/>
      <el-table-column prop="super_month_price" label="超级月卡"/>
      <el-table-column prop="app_promo_super_month_price" label="APP特惠超级月卡" min-width="140"/>
      <el-table-column prop="web_promo_super_month_price" label="WEB特惠超级月卡" min-width="140"/>
      <el-table-column prop="started_at" label="开始时间" width="180"/>
    </el-table>
  </el-card>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { listPriceTasksApi } from '../api'

const statusOptions = [
  { value: 'pending', label: '待处理' },
  { value: 'queued', label: '排队中' },
  { value: 'claimed', label: '已领取' },
  { value: 'processing', label: '处理中' },
  { value: 'success', label: '成功' },
  { value: 'failed', label: '失败' },
  { value: 'cancelled', label: '已取消' }
]
const statusMap = Object.fromEntries(statusOptions.map((item) => [item.value, item.label]))
const statusText = (status) => statusMap[status] || status
const q = reactive({ keyword: '', task_type: '', status: '' })
const items = ref([])

const load = async () => {
  items.value = await listPriceTasksApi(q)
}
const resetSearch = () => {
  Object.assign(q, { keyword: '', task_type: '', status: '' })
  load()
}

onMounted(load)
</script>

<style scoped>
.page-card { border-radius: 16px; }
.page-header { display: flex; justify-content: space-between; gap: 16px; align-items: center; }
.page-title { font-size: 20px; font-weight: 700; color: #1f2937; }
.page-subtitle { margin-top: 4px; color: #6b7280; font-size: 13px; }
.toolbar-form { padding: 4px 0 12px; }
.toolbar-form :deep(.el-form-item) { margin-bottom: 10px; }
.toolbar-form :deep(.el-input), .toolbar-form :deep(.el-select) { width: 220px; }
.responsive-table { width: 100%; border-radius: 12px; overflow: hidden; }
@media (max-width: 768px) {
  .page-header { align-items: flex-start; flex-direction: column; }
  .page-header .el-button { width: 100%; }
  .toolbar-form { display: grid; grid-template-columns: 1fr; }
  .toolbar-form :deep(.el-form-item), .toolbar-form :deep(.el-form-item__content), .toolbar-form :deep(.el-input), .toolbar-form :deep(.el-select) { width: 100%; }
  .toolbar-actions :deep(.el-form-item__content) { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
}
</style>
