Router.configure({
	// 路由配置文件
	layoutTemplate:'layout'
	//加载动画模板
	,loadingTemplate:'loading'
	// 为找到的页面显示页
	,notFoundTemplate:'notFound'
	// 加载动画
	,waitOn:function(){
		// return Meteor.subscribe('posts');
		return [Meteor.subscribe('notifications')]
	}
});
// 第一个参数: url路径;第二个参数：模板名称
// Router.route('/',{name:'postsList'})

Router.route('/posts/:_id',{ 	//查看帖子
	name:'postPage'
	,waitOn:function(){
		return [Meteor.subscribe('singlePost',this.params._id),Meteor.subscribe('comments',this.params._id)]
	}
	,data:function(){
		// this 是当前路由对象
		// console.log(Posts.findOne(this.params._id))
		return Posts.findOne(this.params._id);
	}
})

// Router.route('/posts/:id/edit',{
// 	name:'postEdit'
// 	,data:function(){
// 		return Posts.findOne(this.params._id);
// 	}
// })
Router.route('/posts/:_id/edit',{ 	//查看帖子
	name:'postEdit'
	,waitOn:function(){
		return Meteor.subscribe('singlePost',this.params._id)
	}
	,data:function(){
		// this 是当前路由对象
		return Posts.findOne(this.params._id);
	}
})
// 提交帖子页面
Router.route('/submit',{name:'postSubmit'})
// Route controller通过简单的方式将一组路由特性打包,其他router可以继承
PostsListController = RouteController.extend({
	template:'postsList'
	,increment:5
	,postsLimit:function(){
		return parseInt(this.params.postsLimit) || this.increment;
	}
	,findOptions:function(){
		// return {sort:{submitted:-1},limit:this.postsLimit()};
		return {sort:this.sort,limit:this.postsLimit()};
	}
	// ,waitOn:function(){
	// 	return Meteor.subscribe('posts',this.findOptions());
	// }
	,subscriptions:function(){
		this.postsSub = Meteor.subscribe('posts',this.findOptions());
	}
	,posts:function(){
		return Posts.find({},this.findOptions());
	}
	,data:function(){
		var hasMore = this.posts().count === this.postsLimit();
		// var nextPath = this.route.path({postsLimit:this.postsLimit()+this.increment});

		return {
			posts:this.posts(),
			ready:this.postsSub.ready,
			// nextPath: !hasMore ? nextPath : null
			nextPath:!hasMore ? this.nextPath():null
		};
	}
});

NewPostsController=PostsListController.extend({
	sort:{submitted:-1,_id:-1}
	,nextPath:function(){
		// Router.soutes.newPosts.path 这个对象层级内容
		return Router.routes.newPosts.path({postsLimit:this.postsLimit()+this.increment})
	}
});
BestPostsController=PostsListController.extend({
	sort:{votes:-1,submitted:-1,_id:-1}
	,nextPath:function(){
		return Router.routes.bestPosts.path({postsLimit:this.postsLimit()+this.increment})
	}
})

// Router.route('/:postsLimit?',{
	// 此路由可以匹配所有路由，建议放在最后
	// name:'postsList'
	// ,waitOn:function(){
	// 	var limit=parseInt(this.params.postsLimit) || 5;
	// 	return Meteor.subscribe('posts',{sort:{submitted:-1},limit:limit})
	// }
	// ,data:function(){
	// 	var limit=parseInt(this.params.postsLimit) || 5;
	// 	return {
	// 		posts:Posts.find({},{sort:{submitted:-1},limit:limit})
	// 	}
	// }
// })

Router.route('/',{
	name:'home'
	,controller:NewPostsController
});
Router.route('/new/:postsLimit?',{name:'newPosts'});
Router.route('/best/:postsLimit?',{name:'bestPosts'});

var requireLogin=function(){
	console.log('user',Meteor.user())
	if(!Meteor.user()){
		console.log('loggin',Meteor.login())
		if(Meteor.loggin()){
			this.render(this.loadingTemplate);
		}else{
			this.render('accessDenied');
		}
	}else{
		console.log('go home')
		this.next();
	}
}
// 当路由中的数据data返回falsy时显示无法找到页面
Router.onBeforeAction('dataNotFound',{only:'postPage'})
Router.onBeforeAction(requireLogin,{only:'postSubmit'})