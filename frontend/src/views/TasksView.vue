<template>
  <el-card class="page-card task-page" shadow="never">
    <template #header>
      <div class="page-header">
        <div>
          <div class="page-title">任务列表</div>
          <div class="page-subtitle">可勾选单条或多条任务，批量修改任务字段</div>
        </div>
        <div class="header-actions">
          <el-button type="primary" :disabled="!selectedRows.length" @click="openBatchEdit">批量修改</el-button>
          <el-button @click="exportCsv">导出CSV</el-button>
        </div>
      </div>
    </template>

    <el-form :inline="true" :model="q" class="toolbar-form">
      <el-form-item label="关键词"><el-input v-model="q.keyword" clearable placeholder="任务编号/账号/kugou_id"/></el-form-item>
      <el-form-item label="状态">
        <el-select v-model="q.status" clearable placeholder="全部状态">
          <el-option v-for="s in statusOptions" :key="s.value" :label="s.label" :value="s.value"/>
        </el-select>
      </el-form-item>
      <el-form-item label="任务类型">
        <el-select v-model="q.task_type" clearable placeholder="全部类型">
          <el-option label="充值" value="充值"/>
          <el-option label="查询价格" value="查询价格"/>
        </el-select>
      </el-form-item>
      <el-form-item label="批次ID"><el-input v-model="q.batch_id" clearable/></el-form-item>
      <el-form-item class="toolbar-actions">
        <el-button type="primary" @click="search">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="selection-tip" v-if="selectedRows.length">已选择 {{ selectedRows.length }} 条记录</div>

    <el-table :data="items" stripe class="responsive-table" @selection-change="selectedRows = $event">
      <el-table-column type="selection" width="48" fixed="left"/>
      <el-table-column prop="task_no" label="任务编号" width="190"/>
      <el-table-column prop="account_identifier" label="账号" min-width="150"/>
      <el-table-column prop="account_remark" label="备注" min-width="130"/>
      <el-table-column prop="task_type" label="任务类型" width="100"/>
      <el-table-column prop="plan_type" label="套餐" width="90"/>
      <el-table-column label="状态" width="100">
        <template #default="{row}"><el-tag :type="statusTagType(row.status)">{{ statusText(row.status) }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="progress_status" label="进度说明" min-width="140"/>
      <el-table-column prop="progress_updated_at" label="状态更新时间" width="170"/>
      <el-table-column prop="sale_price" label="售价" width="90"/>
      <el-table-column prop="recharge_cost" label="成本" width="90"/>
      <el-table-column prop="profit" label="利润" width="90"/>
      <el-table-column prop="kugou_id" label="kugou_id" min-width="130"/>
      <el-table-column prop="worker_id" label="worker_id" min-width="120"/>
      <el-table-column prop="uploaded_at" label="上传时间" width="170"/>
      <el-table-column prop="started_at" label="开始时间" width="170"/>
      <el-table-column prop="finished_at" label="完成时间" width="170"/>
      <el-table-column prop="fail_reason" label="失败原因" width="180"/>
      <el-table-column label="操作" width="90" fixed="right">
        <template #default="{row}"><el-button link type="primary" @click="go(row.id)">详情</el-button></template>
      </el-table-column>
    </el-table>

    <div class="pagination-wrap">
      <el-pagination background layout="prev, pager, next" :total="total" v-model:current-page="q.page" v-model:page-size="q.page_size" @current-change="load"/>
    </div>

    <el-dialog v-model="editVisible" :title="`批量修改 ${selectedRows.length} 条任务`" class="edit-dialog" width="860px">
      <el-alert title="勾选字段后才会提交修改；未勾选的字段保持原值。空值会保存为空。" type="info" show-icon :closable="false" class="edit-alert"/>
      <div class="edit-grid">
        <div v-for="field in editableFields" :key="field.key" class="edit-field">
          <el-checkbox v-model="enabledFields[field.key]">{{ field.label }}</el-checkbox>
          <component
            :is="field.component"
            v-model="editForm[field.key]"
            v-bind="field.props"
            :disabled="!enabledFields[field.key]"
            clearable
          >
            <el-option v-for="option in field.options || []" :key="option.value" :label="option.label" :value="option.value"/>
          </component>
        </div>
      </div>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveBatchEdit">保存修改</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { listTasksApi, updateTasksApi } from '../api'

const router = useRouter()
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
const statusTagType = (status) => ({ success: 'success', failed: 'danger', processing: 'warning', claimed: 'info', queued: 'info', cancelled: 'info' }[status] || '')

const field = (key, label, component = 'el-input', props = {}, options = null) => ({ key, label, component, props, options })
const editableFields = [
  field('task_no', '任务编号（仅单条）'),
  field('source_batch_id', '批次ID', 'el-input-number', { min: 1, controlsPosition: 'right' }),
  field('account_identifier', '账号'),
  field('account_remark', '备注'),
  field('plan_type', '套餐类型', 'el-select', { placeholder: '请选择' }, [
    { value: 'month', label: '月卡' }, { value: 'season', label: '季卡' }, { value: 'year', label: '年卡' }
  ]),
  field('task_type', '任务类型', 'el-select', { placeholder: '请选择' }, [
    { value: '充值', label: '充值' }, { value: '查询价格', label: '查询价格' }
  ]),
  field('status', '状态', 'el-select', { placeholder: '请选择' }, statusOptions),
  field('progress_status', '进度说明'),
  field('sale_price', '售价', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('recharge_cost', '成本', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('profit', '利润', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('kugou_id', 'kugou_id'),
  field('validity_value', '有效期数值', 'el-input-number', { min: 0, controlsPosition: 'right' }),
  field('validity_unit', '有效期单位'),
  field('app_month_price', 'APP月卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('app_season_price', 'APP季卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('app_year_price', 'APP年卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('web_month_price', 'WEB月卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('web_season_price', 'WEB季卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('web_year_price', 'WEB年卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('pc_month_price', 'PC月卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('pc_season_price', 'PC季卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('pc_year_price', 'PC年卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('super_month_price', '超级月卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('app_promo_super_month_price', 'APP特惠超级月卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('web_promo_super_month_price', 'WEB特惠超级月卡', 'el-input-number', { min: 0, precision: 2, controlsPosition: 'right' }),
  field('fail_code', '失败代码'),
  field('fail_reason', '失败原因', 'el-input', { type: 'textarea', rows: 2 }),
  field('worker_id', 'worker_id'),
  field('retry_count', '重试次数', 'el-input-number', { min: 0, controlsPosition: 'right' }),
  field('progress_updated_at', '状态更新时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('uploaded_at', '上传时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('queued_at', '排队时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('claimed_at', '领取时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('started_at', '开始时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('finished_at', '完成时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('failed_at', '失败时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' }),
  field('created_at', '创建时间', 'el-date-picker', { type: 'datetime', valueFormat: 'YYYY-MM-DD HH:mm:ss' })
]

const q = reactive({ page: 1, page_size: 20, keyword: '', status: '', task_type: '', batch_id: '' })
const items = ref([])
const total = ref(0)
const selectedRows = ref([])
const editVisible = ref(false)
const saving = ref(false)
const editForm = reactive({})
const enabledFields = reactive({})

const load = async () => {
  const data = await listTasksApi(q)
  items.value = data.items
  total.value = data.total
}
const search = () => {
  q.page = 1
  load()
}
const resetSearch = () => {
  Object.assign(q, { page: 1, page_size: 20, keyword: '', status: '', task_type: '', batch_id: '' })
  load()
}
const go = (id) => router.push(`/tasks/${id}`)
const normalizeValue = (value) => value === '' ? null : value
const openBatchEdit = () => {
  const first = selectedRows.value[0] || {}
  editableFields.forEach(({ key }) => {
    editForm[key] = first[key] ?? ''
    enabledFields[key] = false
  })
  editVisible.value = true
}
const saveBatchEdit = async () => {
  const updates = {}
  editableFields.forEach(({ key }) => {
    if (enabledFields[key]) updates[key] = normalizeValue(editForm[key])
  })
  if (!Object.keys(updates).length) {
    ElMessage.warning('请至少勾选一个要修改的字段')
    return
  }
  if (updates.task_no && selectedRows.value.length > 1) {
    ElMessage.warning('任务编号是唯一字段，只能在勾选单条记录时修改')
    return
  }
  saving.value = true
  try {
    await updateTasksApi({ task_ids: selectedRows.value.map((row) => row.id), updates })
    ElMessage.success('修改成功')
    editVisible.value = false
    await load()
  } finally {
    saving.value = false
  }
}
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

<style scoped>
.page-card { border-radius: 16px; }
.page-header { display: flex; justify-content: space-between; gap: 16px; align-items: center; }
.page-title { font-size: 20px; font-weight: 700; color: #1f2937; }
.page-subtitle { margin-top: 4px; color: #6b7280; font-size: 13px; }
.header-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.toolbar-form { padding: 4px 0 12px; }
.toolbar-form :deep(.el-form-item) { margin-bottom: 10px; }
.toolbar-form :deep(.el-input), .toolbar-form :deep(.el-select) { width: 190px; }
.selection-tip { margin-bottom: 10px; color: #409eff; font-size: 13px; }
.responsive-table { width: 100%; border-radius: 12px; overflow: hidden; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
.edit-alert { margin-bottom: 14px; }
.edit-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; max-height: 58vh; overflow: auto; padding-right: 6px; }
.edit-field { display: flex; flex-direction: column; gap: 6px; }
.edit-field :deep(.el-input), .edit-field :deep(.el-select), .edit-field :deep(.el-input-number), .edit-field :deep(.el-date-editor) { width: 100%; }
@media (max-width: 768px) {
  .page-header { align-items: flex-start; flex-direction: column; }
  .header-actions, .header-actions .el-button { width: 100%; }
  .toolbar-form { display: grid; grid-template-columns: 1fr; }
  .toolbar-form :deep(.el-form-item), .toolbar-form :deep(.el-form-item__content), .toolbar-form :deep(.el-input), .toolbar-form :deep(.el-select) { width: 100%; }
  .toolbar-actions :deep(.el-form-item__content) { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .pagination-wrap { justify-content: center; overflow-x: auto; }
  .edit-grid { grid-template-columns: 1fr; max-height: 60vh; }
  :deep(.edit-dialog) { width: calc(100vw - 24px) !important; }
}
</style>
