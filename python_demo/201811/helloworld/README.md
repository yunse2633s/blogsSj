# 说明文档

> 这个helloword 是用什么创建的
	由Django 
> 如何运行
	$ python manage.py runserver 8000
> 参照文献是什么
	参考 麦子学院 python开发
> 如何安装Django呢? 请看官网

> 如何检验Dj的安装？ 

 进入python命令行 ，{
	>>>import django 
	>>>django.VERSION
 }
 > 使用什么ide（跨平台的编辑器）呢？
	Pycharm, sublimie, 
 > 如果建立 Django 项目呢

 $ django-admin startproject myApp(文件夹名字)
    django-admin创建了myApp的文件夹，其中有一些文件和文件夹
    {
    	__init__.py：表示python模块
    	settings.py： web设置文件
	    urls.py：网址映射文件
	    view.py：
	    wsgi.py： 网址接口文件
    }
    
$ python manage.py startapp blog(模块名)
	文档结构
	{
		__init__.py:
		migrations:
		tests.py:测试用例
		views.py：视图
		admin.py：管理
		models.py：数据库模型
	}

> python3 和 python2.7的路由有什么不同
> django 建库、建表
	$ python manage.py makemigrations  # 初始化/重新建库建表
	$ python manage.py migrate  # 建库建表同步到数据库中
	$ python manage.py createsuperuser # 创建后台管理员账户 admin 111111
	在urls中增加 admin的路由
	`
	url(r'^admin/$', include(admin.site.urls)),
	`
	模块中有一个models.py文件，可以在其中建表
> django.db.ImageField 提示 pillow 问题
### error 
	若不安装pillow组件，ImageFileld存在问题

# 20181126 
	因blog的路由失败,参照《python...》重新测试learning_log
 

# 略读python中的django之后
 	1, urls.py中如何引用其他应用中的urls文件
 	
 	2, 如何创建base模板，是否可以直接写html源文件
 	 > `template tag`使用 
 	 	{% tag %} {% endtag %}
 	 	{% extends %}
 	 	{# 注释 #}
 	 	{{ values }}
 	 	过滤器Filters {{ name|lower }}

### error
	1. ModuleNotFoundError: No module named 'bootstrap3blog'
	修改settings.py中的INSTALLED_APPS值，忘记(',')逗号，启动报错
	2. 