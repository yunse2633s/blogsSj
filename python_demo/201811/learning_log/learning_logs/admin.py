from django.contrib import admin

# Register your models here.

# 导入要注册的模型Topic
from learning_logs.models import Topic, Entry
# 允许管理后台管理 Topic模型
admin.site.register(Topic)

admin.site.register(Entry)