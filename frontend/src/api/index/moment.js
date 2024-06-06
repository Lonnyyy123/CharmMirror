/**
 * api
 */
import axios from '@/utils/request.js'

const api = {
  listApi: '/myapp/index/moment/list',
  createApi: '/myapp/index/moment/create'
}

export const createApi = function (data) {
  return axios({
    url: api.createApi,
    method: 'post',
    headers: {
      'Content-Type': 'application/form-data'
    },
    data: data
  })
}
/**
 * list
 */
export const listApi = function (data) {
  return axios({
    url: api.listApi,
    method: 'get',
    params: data
  })
}
