Router.configure({
	// 路由配置文件
	layoutTemplate:'layout'
	//加载动画模板
	,loadingTemplate:'loading'
	// 为找到的页面显示页
	,notFoundTemplate:'notFound'
	// 加载动画
	,waitOn:function(){
		return Meteor.subscribe('posts');
	}
});
// 第一个参数: url路径;第二个参数：模板名称
Router.route('/',{name:'postsList'})
Router.route('/posts/:_id',{
	name:'postPage'
	,data:function(){
		// this 是当前路由对象
		console.log(this)
		return Posts.findOne(this.params._id)
	}
})


// 提交帖子页面
Router.route('/submit',{name:'postSubmit'})

var requireLogin=function(){
	if(!Meteor.user()){
		if(Meteor.loggin()){
			this.render(this.loadingTemplate);

		}else{
			this.render('accessDenied');
		}
	}else{
		this.next()
	}
}
// 当路由中的数据data返回falsy时显示无法找到页面
Router.onBeforeAction('dataNotFound',{only:'postPage'})
Router.onBeforeAction(requireLogin,{only:'postSubmit'})