import request from '../utils/request'

export const loginApi = (data) => request.post('/api/auth/login', data)
export const dashboardStatsApi = () => request.get('/api/dashboard/stats')
export const importTasksApi = (formData) => request.post('/api/tasks/import', formData)

export const listTasksApi = (params = {}) => {
  const cleanedParams = {
    page: params.page,
    page_size: params.page_size
  }

  if (params.keyword !== '' && params.keyword != null) {
    cleanedParams.keyword = params.keyword
  }

  if (params.status !== '' && params.status != null) {
    cleanedParams.status = params.status
  }

  if (params.batch_id !== '' && params.batch_id != null) {
    cleanedParams.batch_id = params.batch_id
  }

  return request.get('/api/tasks', { params: cleanedParams })
}

export const getTaskApi = (id) => request.get(`/api/tasks/${id}`)
export const listBatchesApi = () => request.get('/api/batches')
export const getBatchApi = (id) => request.get(`/api/batches/${id}`)