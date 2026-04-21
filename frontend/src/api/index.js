import request from '../utils/request'

export const loginApi = (data) => request.post('/api/auth/login', data)
export const dashboardStatsApi = () => request.get('/api/dashboard/stats')
export const importTasksApi = (formData) => request.post('/api/tasks/import', formData)
export const listTasksApi = (params) => request.get('/api/tasks', { params })
export const getTaskApi = (id) => request.get(`/api/tasks/${id}`)
export const listBatchesApi = () => request.get('/api/batches')
export const getBatchApi = (id) => request.get(`/api/batches/${id}`)
