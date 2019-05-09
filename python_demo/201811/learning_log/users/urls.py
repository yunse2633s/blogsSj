from django.urls import path, re_path
# from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from . import views

app_name='users'

urlpatterns=[

	# 登陆
	# path('login/', login,  name='login'),
	path('login/', LoginView.as_view(template_name='users/login.html'),name='login'),

	# 注销
	path('logout/', views.logout_view, name='logout'),

	# 注册页面
	path('register/', views.register, name='register'),

	# 注册页面
	path('test/', views.test, name='test'),

	
]