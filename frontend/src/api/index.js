import request from '../utils/request'

export const loginApi = (data) => request.post('/api/auth/login', data)
export const dashboardStatsApi = () => request.get('/api/dashboard/stats')
export const importTasksApi = (formData) => request.post('/api/tasks/import', formData)
export const listTasksApi = (params = {}) => {
  const normalizeValue = (value) => (typeof value === 'string' ? value.trim() : value)
  const keyword = normalizeValue(params.keyword)
  const status = normalizeValue(params.status)
  const batchId = normalizeValue(params.batch_id)
  const cleanedParams = {
    page: params.page ?? 1,
    page_size: params.page_size ?? 20
  }

  if (keyword !== '' && keyword != null) {
    cleanedParams.keyword = keyword
  }

  if (status !== '' && status != null) {
    cleanedParams.status = status
  }

  if (batchId !== '' && batchId != null) {
    cleanedParams.batch_id = batchId
  }

  return request.get('/api/tasks', { params: cleanedParams })
}
export const getTaskApi = (id) => request.get(`/api/tasks/${id}`)
export const listBatchesApi = () => request.get('/api/batches')
export const getBatchApi = (id) => request.get(`/api/batches/${id}`)
