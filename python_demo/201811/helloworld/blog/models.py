from django.db import models

# Create your models here.
# 
# class blog(models.Model):
#     name = models.CharField(max_length=20)

class Author(models.Model):
    name = models.CharField(max_length=20)
    age=models.IntegerField(default=18)

class Article(models.Model):
    
    title=models.CharField(max_length=200)
    content=models.TextField()
    url=models.URLField()
    portal=models.ImageField(upload_to="icons") #若不安装pillow组件，ImageFileld存在问题
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    
