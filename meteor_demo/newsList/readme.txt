##Meteor文件结构
1，
	/client:(仅客户端运行)
	/server:(仅服务端运行)
	/public:(静态文件)
	/lib
	.meteor/packages 列出你所安装的代码包
	.meteor/release:列出你使用的meteor版本
##读取顺序
1，/lib/ > main.* >字母排序
##命名法则
1，本例采用驼峰命名法

##项目目标
1,实现BBS的功能

## minimongo
###控制台命令
>Posts.find().fetch()
>Posts.insert({
	'title':'A second'
	,'url':'http://ww.baidu.com'
})
>Posts.find().count()
###初始化数据库
meteor reset
### 关闭自动发布 或称为"订阅"
meteor remove autopublish
>DDP:分布式数据协议(Distributed Data Protocol)
### 路由常用词
路由规则、路径、目录、hooks、过滤器、路由模板、布局、控制器
1，在template文件夹中创建layout模板,使用标签{{> yield}} 调用
2，增加一个加载动画
meteor add sacha:spin
使用 {{> spinner}}  调用
###自动跟踪响应式数据源
1，autorun
Tracker.autorun(function(){
	console.log('value'+Session.get('titile'))
})
当session每次发生变化的时候，均会调用autorun
2,响应式
实时性的方法是通过使用.observe()实现，当指向数据的指针发生改变时就会触发回调。而meteor通过这个回调更改DOM
3,依赖跟踪:computations
Meteor.startup(function(){
// 当meteor完成加载Posts集合后只运行tracker一次
	Tracker.autorun(function(){
		console.log('there are'+Posts.find().count() + 'posts')
	})
})
###发布信息
1,添加安全检查
使用 audit-argument-checks包,增加字符串校验
如；check(Meteor.userId(),String)
2,使用Underscore库的_.extend()将一个对象的属性传递给另一个对象
exam:_.extend(postAttributes,{a:'b'})
###防止重复
	数据发送到服务端前先进行服务端查询，若存在则终止否则添加
###帖子排序
	使用monogdb总的排序
	{sort:{data:-1}}

###用法
1. Tempalte.postEdit(模板名称).events({
	'事件 元素':function(e){
		//
	}
})
	如:
		事件:submit click mouseout 
		元素:标签、class、id
	Tempalte.postEdit.events({
	'submit form':function(e){
		//
	}
})

###模板渲染
Template.error.rendered=function(){
	
}
###meteor定期器
Meteor.setTimeout(function(){},3000)