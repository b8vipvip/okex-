<template>
  <el-card>
    <el-table :data="items">
      <el-table-column prop="batch_no" label="批次编号" width="190"/>
      <el-table-column prop="batch_name" label="批次名称"/>
      <el-table-column prop="total_count" label="总数"/>
      <el-table-column prop="success_count" label="成功数"/>
      <el-table-column prop="failed_count" label="失败数"/>
      <el-table-column prop="pending_count" label="待处理"/>
      <el-table-column prop="created_at" label="创建时间" width="180"/>
    </el-table>
  </el-card>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { listBatchesApi } from '../api'
const items = ref([])
onMounted(async()=> items.value = await listBatchesApi())
</script>
