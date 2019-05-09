"""
from django.http import HttpResponse
 
def hello(request):
    return HttpResponse("Hello world ! ")
    """
# 使用模板 templates
from django.shortcuts import render
 
def hello(request, year):
    print(year)
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def ifor(request):
    context          = {}
    context['hello'] = 'Hello World!'
    context['condition'] = '1'
    context['athlete_list'] = [1,2,3,4]
    
    return render(request, 'ifor.html', context)