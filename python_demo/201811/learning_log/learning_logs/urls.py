""" 定义learning_logs 的url模式 """
from django.urls import path, re_path
from . import views

# 命名空间
app_name='learning_logs' 

urlpatterns = [
	# 主页
	path('', views.index, name='index'),

	# 查询 显示所有主题
	path('topics/', views.topics, name='topics'),

	# `r` 将这个字符串视为原始字符串
	#  `?P<topic_id>` 将比配的值存储在topic_id中
	#  查询
	re_path(r'^topic/(?P<topic_id>\d+)/$', views.topic, name='topic'),

	# 添加 一个新的topic，用户使用
	path('new_topic/', views.new_topic, name='new_topic'),

	# 添加 新的entry
	re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

	# 编辑 entry
	re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

	#
]
