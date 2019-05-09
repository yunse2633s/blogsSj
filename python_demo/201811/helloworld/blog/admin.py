from django.contrib import admin

from blog.models import *
# Register your models here.
# 
# 编写admin.site.register()的目的
admin.site.register(Article)
admin.site.register(Author)