# 子应用的路由
from django.urls import path
from . import views
# 定义命名空间
# 
app_name='blog'

urlpatterns=[

	path('gbye/', views.goodbye, name='gbye'),

]