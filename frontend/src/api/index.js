import request from '../utils/request'

const cleanParams = (params = {}) =>
  Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== '' && v !== null && v !== undefined)
  )

export const loginApi = (data) => request.post('/api/auth/login', data)
export const dashboardStatsApi = () => request.get('/api/dashboard/stats')
export const importTasksApi = (formData) => request.post('/api/tasks/import', formData)
export const listTasksApi = (params) => request.get('/api/tasks', { params: cleanParams(params) })
export const getTaskApi = (id) => request.get(`/api/tasks/${id}`)
export const listBatchesApi = () => request.get('/api/batches')
export const getBatchApi = (id) => request.get(`/api/batches/${id}`)
