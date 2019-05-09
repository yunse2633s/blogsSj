from django.shortcuts import render

# new_topic
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse # python2.7+django1.*
# https://docs.djangoproject.com/en/2.1/ref/urlresolvers/
from django.urls import reverse   # django2.1

from .forms import TopicForm, EntryForm

# 导入与数据相关联的模型
from .models import Topic, Entry

# 使用Django提供的装饰器，限制用户访问
from django.contrib.auth.decorators import login_required

# 测试装饰器
from learning_log.decorators import test_decorator
# Create your views here.

def index(request):
	""" 主页 """
	return render(request, 'learning_logs/index.html')

# 增加装饰器(@login_required)，限制未登陆用户访问; 即运行topics之前先运行login_required
@login_required
def topics(request):
	""" 显示所有 topic数据 """
	# topics = Topic.objects.order_by('date_added')
	# 只允许用户访问自己的主题数据
	print('user', request.user)
	for i in request:
		print('request', i)

	topics=Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}

	return render(request, 'learning_logs/topics.html', context)


# GET请求，传参 topic_id ，与urls.py中的路由对应
# @test_decorator
def topic(request, topic_id):
	"""显示单个主题及其所有的条目"""
	# `get`: 数据模型的方法
	topic = Topic.objects.get(id=topic_id)
	
	# 确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404

	# `entry_set` : 为通过外键关系获取数据，可以使用相关模型的小写名称、下划线和单词(set)调用相关方法
	entries = topic.entry_set.order_by('-date_added')

	context = {'topic': topic, 'entries': entries}

	return render(request, 'learning_logs/topic.html', context)
	
# 
# new_topic() 需要处理有参数和无参数两种情况，并作出相应的跳转
# 需要 HttpResponseRedirect, reverse
def new_topic(request):
	""" 添加新主题 """
	if request.method != 'POST':
		# 未提交数据：创建一个新表单
		form = TopicForm()
	else:
		#
		form = TopicForm(request.POST)
		if form.is_valid():
			# form.save()
			# 增加额外参数
			# 参数commit=False,先保存到本地，再提交到数据库中
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context={'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

# 
# 创建 entry 数据
# 
def new_entry(request, topic_id):
	""" 在特定的主题中添加新条目 """
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		# 未提交数据，创建一个空表单
		form = EntryForm()
	else:
		# POST提交数据，进行处理
		form = EntryForm(data=request.POST)
		if form.is_valid():
			# 参数commit=False，创建对象，并存储到new_entry中，但不保存到数据库中。
			new_entry=form.save(commit=False)
			new_entry.topic=topic
			# 如果topic.owner!=request.user, 则提示非法者

			# save() 将new_entry保存到数据库
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

	context={'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)


#
# 编辑 entry
# 
def edit_entry(request, entry_id):
	"""编辑既有条目"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	
	# 确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
	# 初次请求，使用当前条目填充表单, 创建实例
		form = EntryForm(instance=entry)

	else:
		# POST提交的数据，对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)

		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}

	return render(request, 'learning_logs/edit_entry.html', context)