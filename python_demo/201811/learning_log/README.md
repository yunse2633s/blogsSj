`
	系统环境: win10 + python3.7 + Django2.1.3
`

# 创建项目
	>django-admin startproject learning_log .
	根目录(.)下生成一个文件夹(learning_log)

# 创建数据库
	>python manage.py migrate
	
# 安装 sqlite

# 如何打开db.sqlite3文件
	>sqlite3 db.sqlite3 	#打开db.sqlite3数据库文件
	>.table 		#查询数据库中的表
	>.schema 		#查看建表语句

# 查看项目 允许项目
	> python manage.py runserver
	>浏览器中访问,默认8000端口

# 创建learning_logs应用程序
	> python manage.py startapp learning_logs

# 定义数据模型 
	打开learning_logs应用中的models.py

# 激活模型
	> 将应用程序(learning_logs)包含到项目中,打开learning_log/learning_log中的settings.py。
	> 修改数据库，
		>@ 使用关键词 `makemigrations`,创建迁移文件(其存储新模型相关链的数据)
		> python manage.py makemigrations learning_logs
		>@ 应用迁移，修改数据库
		> python manage.py migrate

# Django 自带管理后台，创建超级用户
	> python manage.py createsuperuser

# 向管理后台注册模型
	Django自动添加了User 和 Group,用户自己的需要手动注册。
	> 在learning_logs应用文件中创建admin.py文件, 添加数据模型
	> 运行该项目，并登陆后台,http://127.0.0.1:8000/admin

# 定义数据模型，并与上一个数据模型进行关联
	> models.py 
	> TIP: 自动创建索引字段`id`, 
# 修改数据库，迁移，修改，注册
## error
` TypeError: __init__() missing 1 required positional argument: 'on_delete' `
多对一的关系，需要两个位置参数：模型相关的类和on_delete选项。（on_delete实际上并不需要，但是不提供它会给出弃用警告，这在Django 2.0中将是必需的，1.8及以前的版本不需要）
{
	in可参照：
https://docs.djangoproject.com/en/2.1/ref/models/fields/
https://blog.csdn.net/pugongying1988/article/details/72870264
}

## sqlite3 命令
	> 查看`entry`表结构
	select * from sqlite_master where type='table' and name='learning_logs_entry'
	> 删除表
		drop table 表名;
		：若是django创建的还需要删除另外两表中的相关信息；(*_migrations, *_content_type)
	> 删除行
		delete from 表名 where 条件

# error： models中字符数不足，导致添加数据失败	
	
# 创建网页
	>3阶段： 
		定义url(urls.py)、 
		编写视图(views.py)、 
		编写模板(templates\myApp\*.html)
	> error
		在子应用中创建urls.py时，需要定义它的命名空间
		如：`.\learning_logs\urls.py` 中的 app_name
	> 模板继承
	 {% url 'learing_logs:index' %}
	 {% block AAA %} {% endblock AAA %}
	 {% extends "learing_logs/base.html" %}
	 `
	{% for item in items %} 
		{% empty %}
	{% endfor %}
	 `
	 > GET 路由传参, urls 中发送 和views中接受
	 > 如何查询数据库
	 	导入数据模型，使用模型类中方法
	 > 数据库模型下的方法：（这部分的说明请查看 Django API）

		A*.objects.all()
		A*.objects.get()
		A*.B*_set.all()  #B* 表示A与B存在外键关联, 

# 表单操作 `forms`  和 数据添加
	> forms.ModelForm
	> 内嵌Meta类
	> *.save

# 过滤器的用法
	> date
	> linebreaks

# 表单操作 和 数据修改

# 创建用户
	> 创建users应用
		python manage.py startapp users
	> 在settings.py中添加 users. INSTALLED_APPS
	> 在根目录中的urls.py中，增加users的url
	> 在usres应用目录下创建urls.py
	> 登陆、注销、注册
	> 使用装饰器，限制未登陆用户访问: 写法：@+函数名，它类似某方法的前置操作
		`@login_required`
		如何全部限制？是否可以只是用一个装饰器限制多个方法呢？
	> 重定向。 例：若用户未登陆，则跳转到登陆页面
		在引导目录中找到setttings.py,在文档最后写` LOGIN_URL='' `
	> 设置数据与用户的关系；即只能查阅自己的数据

# 应用bootstrap
	> pin install django-bootstrap3
	> 应用django-bootstrat3
	说明文档：
	https://django-bootstrap3.readthedocs.io/en/latest/



# django1.* -- django2.1*
	>使用Django提供的默认登陆视图
		1.*版 {
			from django.contrib.auth views import login
			...
			urlpathtters=[
				url((r'^login/$', login, {'template_name': 'users/login.html'}, name='login')
			]
		}
		2.* 版 {
			from django.contrib.auth.views import LoginView
			path('login/', LoginView.as_view(template_name='users/login.html'),name='login'),
		}

	> url 和path的用法
		1.* 版{
			非正则 url(r'^$')
			正则 url()
		}
		2.* 版{
			非正则 path('')
			正则 re_path()
		}
	> namespace命名空间
		1.* 版{ 
			无
		}
		2.* 版{
			需要在urls.py中定义 app_name='nameSpace'
		}
	> 外键关联
		1.* 版{ 
			B = models.ForeignKey(A)
		}
		2.* 版{
			# 需要增加on_delete属性
			B = models.ForeignKey(A,  'on_delete=models.CASCADE')
		}
	> 异常处理
		1.* 版{
			try:
				...
			except Exception,e:
				...
		}
		2.* 版{
			try:
				...
			except Exception as e:
				...
		}
# Django下的数据操作
	>重建数据库
	> 迁移数据库
	> shell环境下操作数据