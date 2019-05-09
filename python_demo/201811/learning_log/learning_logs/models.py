from django.db import models
# 将数据关联上用户
from django.contrib.auth.models import User
# Create your models here.

# 创建Topic类，继承Model(Model是Django中定义了模型基本功能的类)
# 用于存放列表信息
# 关联用户数据
class Topic(models.Model):
	"""用户学习的主题"""
	# max_length设置200个字符
	text = models.CharField(max_length=200)
	# auto_now_add 创建时，自动设置当前日期
	date_added = models.DateTimeField(auto_now_add=True)
	# 关联用户信息, 只能自己查看自己的数据
	owner = models.ForeignKey(User, 'on_delete=models.CASCADE')
	# __str__() 返回存储在属性text中的字符串 python2.7中使用 __unicode__()
	def __str__(self):
		"""返回模型的字符串表示"""
		return self.text


# 用于存放详情
#
# class Entry(models.Model):
# 	"""学到的有关某个主题的具体知识"""
# 	topic = models.ForeignKey(Topic)
# 	text = models.TextField()
# 	date_added = models.DateTimeField(auto_now_add=True)

# 	# 嵌套 Meta类
# 	class Meta:
# 		verbose_name_plural = 'entries'

# 	def __str__(self):
# 		"""返回模型的字符串表示，且返回前50个字符,并添加省略号"""
# 		return self.text[:50] + "..."

class Entry(models.Model):
	topic = models.ForeignKey('Topic', 'on_delete=models.CASCADE')
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'

	def __str__(self):
		# 若不足50个字符程序会报错
		# return self.text[.50]+"..."
		return self.text