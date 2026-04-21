<template>
  <el-card v-if="task">
    <h3>任务 {{ task.task_no }}</h3>
    <el-descriptions :column="2" border>
      <el-descriptions-item label="账号">{{task.account_identifier}}</el-descriptions-item>
      <el-descriptions-item label="备注">{{task.account_remark}}</el-descriptions-item>
      <el-descriptions-item label="状态">{{displayStatus(task)}}</el-descriptions-item>
      <el-descriptions-item label="实时状态更新时间">{{task.progress_updated_at}}</el-descriptions-item>
      <el-descriptions-item label="worker">{{task.worker_id}}</el-descriptions-item>
      <el-descriptions-item label="售价">{{task.sale_price}}</el-descriptions-item>
      <el-descriptions-item label="成本">{{task.recharge_cost}}</el-descriptions-item>
      <el-descriptions-item label="利润">{{task.profit}}</el-descriptions-item>
      <el-descriptions-item label="失败">{{task.fail_reason}}</el-descriptions-item>
    </el-descriptions>
    <h4 style="margin-top:16px">日志</h4>
    <el-timeline>
      <el-timeline-item v-for="l in task.logs" :key="l.id" :timestamp="l.created_at">{{l.content}}</el-timeline-item>
    </el-timeline>
  </el-card>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getTaskApi } from '../api'
const route = useRoute()
const task = ref(null)
const displayStatus = (taskData) => taskData?.progress_status || taskData?.status_text || taskData?.status
onMounted(async()=> task.value = await getTaskApi(route.params.id))
</script>
