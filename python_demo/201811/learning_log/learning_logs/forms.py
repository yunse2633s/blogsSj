# 导入模块 forms
from django import forms
# 导入模型 Topic
from .models import Topic, Entry

# 定义TopicForm类，并继承forms.ModelForm
class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['text']
		labels = {'text': ''}

# 定义EntryForm类，并继承forms.ModelForm
# 
class EntryForm(forms.ModelForm):
	# 简单的ModelForm中只包含一个内嵌Meta类，它将指明使用那个模型建表单，以及表单中包含哪些字段。
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text': ''}
		# widgets是html表单元素，如单行文本框、多行文本区域、 下拉列表，它可以覆盖Django默认的部件
		widgets = {'text': forms.Textarea( attrs={'cols': 80} )} # cols默认40

#