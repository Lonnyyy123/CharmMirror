from django.urls import path

from myapp import views

app_name = 'myapp'
urlpatterns = [
    path('admin/loginLog/list', views.admin.loginLog.list_api),
    path('admin/loginLog/create', views.admin.loginLog.create),
    path('admin/loginLog/update', views.admin.loginLog.update),
    path('admin/loginLog/delete', views.admin.loginLog.delete),
    path('admin/opLog/list', views.admin.opLog.list_api),
    path('admin/errorLog/list', views.admin.errorLog.list_api),
    path('index/user/login', views.index.user.login),
    path('index/user/register', views.index.user.register),
    path('index/user/info', views.index.user.info),
    path('index/user/update', views.index.user.update),
    path('index/user/updatePwd', views.index.user.updatePwd),
    path('index/moment/list', views.index.moment.list_api),
    path('index/operations/bigeye', views.index.operations.bigeye),
    path('index/operations/thin', views.index.operations.thin),
    path('index/operations/smooth', views.index.operations.smooth),
    path('index/operations/whiten', views.index.operations.whiten),
    path('index/moment/create', views.index.moment.create),
]
