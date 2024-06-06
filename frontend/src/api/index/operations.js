/**
 * api
 */
import axios from '@/utils/request.js'

const api = {
  smoothApi:'/myapp/index/operations/smooth',
  thinApi:'/myapp/index/operations/thin',
  bigeyeApi:'/myapp/index/operations/bigeye',
  whitenApi:'/myapp/index/operations/whiten'
}

export const smoothApi = function (data) {
  return axios({
    url: api.smoothApi,
    method: 'post',
    data: data
  })
}
export const thinApi = function (data) {
  return axios({
    url: api.thinApi,
    method: 'post',
    data: data
  })
}
export const bigeyeApi = function (data) {
  return axios({
    url: api.bigeyeApi,
    method: 'post',
    data: data
  })
}
export const whitenApi = function (data) {
  return axios({
    url: api.whitenApi,
    method: 'post',
    data: data
  })
}

