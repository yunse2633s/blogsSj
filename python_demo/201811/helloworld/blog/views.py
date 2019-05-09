# from django.shortcuts import render

# # Create your views here.
# # 
# def goodbye(request):
    
#     context          = {}
#     context.hello='未来已来'
#     return render(request, 'hello.html', context)
#     
#     
    
from django.http import HttpResponse

def goodbye(request):
	return HttpResponse("<h1>blog</h1>")