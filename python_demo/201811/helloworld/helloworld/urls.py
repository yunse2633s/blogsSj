"""helloworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
    https://docs.djangoproject.com/zh-hans/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
#example:

# python3.0
from django.contrib import admin

# 为何要用 path呢
from django.urls import path, include

from django.conf.urls import url

from . import view

# 如何链接其他文件模块下的路径呢
# 
urlpatterns = [
	# path('hello/', view.hello),
    
 #    path('hello/<int:year>/', view.hello), # hello()中要有对应的参数
	# path('ifor/', view.ifor),
    path('admin/', admin.site.urls),
    # path('blog/', blog.views.goodbye),
    # path('', include('blog.urls.py', namespace='blog')), # 错误
    path('', include('blog.urls', namespace='blog')),
    # url(r'^hello/$', view.hello),
    url(r'^hello/([0-9]{4})/$', view.hello),
    url(r'^ifor/', view.ifor),
    # url(r'^blog/', 'blog.views.goodbye')
    # 
    

]

"""
# python 2.7
from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'^$', view.hello),
]
"""