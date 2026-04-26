<template>
  <el-row :gutter="12">
    <el-col :span="6" v-for="k in cards" :key="k.key"><el-card><div>{{k.label}}</div><h2>{{stats[k.key] ?? 0}}</h2></el-card></el-col>
  </el-row>
</template>
<script setup>
import { onMounted, reactive } from 'vue'
import { dashboardStatsApi } from '../api'
const stats = reactive({})
const cards = [
  { key: 'total_tasks', label: '总任务' },
  { key: 'queued', label: 'Queued' },
  { key: 'claimed', label: 'Claimed' },
  { key: 'processing', label: 'Processing' },
  { key: 'success', label: 'Success' },
  { key: 'failed', label: 'Failed' },
  { key: 'sale_total', label: '总销售额' },
  { key: 'cost_total', label: '总成本' },
  { key: 'profit_total', label: '总利润' }
]
onMounted(async()=>Object.assign(stats, await dashboardStatsApi()))
</script>
