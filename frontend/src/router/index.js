import Vue from 'vue'
import Router from 'vue-router'

// 重复点击bug
const originalPush = Router.prototype.push

Router.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(Router)

const constantRouterMap = [
  // ************* 前台路由 **************
  {
    path: '/',
    redirect: '/index'
  },
  {
    path: '/index',
    name: 'index',
    redirect: '/index/portal',
    component: () => import('@/views/index'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('@/views/index/login')
      },
      {
        path: 'picture-edit',
        name: 'picture-edit',
        component: () => import('@/views/index/editor/picture-edit')
      },
      {
        path: 'portrait-edit',
        name: 'portrait-edit',
        component: () => import('@/views/index/editor/portrait-edit')
      },
      {
        path: 'social-plaza',
        name: 'social-plaza',
        component: () => import('@/views/index/social-plaza')
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('@/views/index/register')
      },
      {
        path: 'portal',
        name: 'portal',
        component: () => import('@/views/index/portal')
      },
      {
        path: 'detail',
        name: 'detail',
        component: () => import('@/views/index/detail')
      },
      {
        path: 'search',
        name: 'search',
        component: () => import('@/views/index/search')
      },
      {
        path: 'user',
        name: 'user',
        redirect: 'user/addressView',
        component: () => import('@/views/index/user'),
        children: [
          {
            path: 'userInfoEditView',
            name: 'userInfoEditView',
            component: () => import('@/views/index/user/userinfo-edit-view')
          },
          {
            path: 'followView',
            name: 'followView',
            component: () => import('@/views/index/user/follow-view')
          },
          {
            path: 'fansView',
            name: 'fansView',
            component: () => import('@/views/index/user/fans-view')
          },
          {
            path: 'scoreView',
            name: 'scoreView',
            component: () => import('@/views/index/user/score-view')
          },
          {
            path: 'commentView',
            name: 'commentView',
            component: () => import('@/views/index/user/comment-view')
          },
          {
            path: 'securityView',
            name: 'securityView',
            component: () => import('@/views/index/user/security-view')
          },
          {
            path: 'pushView',
            name: 'pushView',
            component: () => import('@/views/index/user/push-view')
          },
          {
            path: 'messageView',
            name: 'messageView',
            component: () => import('@/views/index/user/message-view')
          }
        ]
      }
    ]
  }
]

export default new Router({
  routes: constantRouterMap
})
