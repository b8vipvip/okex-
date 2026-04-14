import axios from 'axios'
import { ElMessage } from 'element-plus'

const instance = axios.create({ baseURL: '/', timeout: 15000 })

instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

instance.interceptors.response.use(
  (resp) => {
    const payload = resp.data
    if (payload.code !== 0) {
      ElMessage.error(payload.message || '请求失败')
      return Promise.reject(payload)
    }
    return payload.data
  },
  (err) => {
    ElMessage.error(err.response?.data?.message || err.message || '网络错误')
    return Promise.reject(err)
  }
)

export default instance
