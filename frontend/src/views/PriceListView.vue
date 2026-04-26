<template>
  <el-card>
    <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
      <b>账号最新价格列表（查询价格任务）</b>
      <el-button @click="load">刷新</el-button>
    </div>
    <el-table :data="items" stripe>
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
      <el-table-column prop="started_at" label="查询时间" width="180"/>
    </el-table>
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { listPriceTasksApi } from '../api'

const items = ref([])

const load = async () => {
  items.value = await listPriceTasksApi()
}

onMounted(load)
</script>
