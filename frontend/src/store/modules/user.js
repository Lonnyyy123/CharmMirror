import storage from 'store'
import { loginApi } from '@/api/index/user'
import {ADMIN_TOKEN, ADMIN_USERNAME, TOKEN, USERNAME, USERID} from '@/store/constants'

const user = {
  namespaced: false,
  state: {
    /** 前台字段 **/
    token: '',
    username: '',
    userId: '',

    /** 管理员字段**/
    adminToken: '',
    adminUserName: ''
  },
  getters: {
    token: state => state.token,
    username: state => state.username,
    userId: state => state.userId,
  },
  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_USERID: (state, userId) => {
      state.userId = userId
    }
  },

  actions: {
    // 普通用户登录
    Login ({commit}, {username, password}) {
      return new Promise((resolve, reject) => {
        loginApi({
          username,
          password
        }).then(response => {
          const result = response.data
          commit('SET_TOKEN', result.token)
          commit('SET_USERNAME', result.username)
          commit('SET_USERID', result.id)
          storage.set(TOKEN, result.token)
          storage.set(USERNAME, result.username)
          storage.set(USERID, result.id)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 普通用户退出
    Logout ({ commit, state }) {
      return new Promise((resolve) => {
        commit('SET_TOKEN', '')
        commit('SET_USERNAME', '')
        commit('SET_USERID', '')
        storage.remove(TOKEN)
        storage.remove(USERNAME)
        storage.remove(USERID)
        resolve()
      })
    }
  }
}

export default user
