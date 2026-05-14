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

  if (params.task_type !== '' && params.task_type != null) {
    cleanedParams.task_type = params.task_type
  }

  if (params.batch_id !== '' && params.batch_id != null) {
    cleanedParams.batch_id = params.batch_id
  }

  return request.get('/api/tasks', { params: cleanedParams })
}

export const getTaskApi = (id) => request.get(`/api/tasks/${id}`)
export const listBatchesApi = () => request.get('/api/batches')
export const getBatchApi = (id) => request.get(`/api/batches/${id}`)
export const updateTasksApi = (data) => request.patch('/api/tasks/batch', data)

export const listPriceTasksApi = (params = {}) => {
  const cleanedParams = {}
  ;['keyword', 'status', 'task_type'].forEach((key) => {
    if (params[key] !== '' && params[key] != null) cleanedParams[key] = params[key]
  })
  return request.get('/api/tasks/price-list', { params: cleanedParams })
}
