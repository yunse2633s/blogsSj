Meteor.publish('posts',function(options){
	check(options,{
		sort:Object
		,limit:Number
	});
	return Posts.find({},options);
	// 查询flagged字段为false的记录
	// return Posts.find({flagged:false})
	// Posts.find({flagged:false,author:author})
})
Meteor.publish('singlePost',function(id){
	check(id,String)
	return Posts.find(id);
})
// 尝试在Posts.find()后更上observe方法会出现什么样的结果,下列代码在server||client?
/**
Posts.find().observe({
	added:function(post){
		$('ul').append('<li id="' + post._id + '">') + post.title + '</li>')
	},
	changed:function(post){
		$('ul li#' + post._id).text(post.title)
	},
	removed:function(post){
		$('ul li#' + post._id).remove()
	}
})
*/
// 发布评论
Meteor.publish('comments',function(postId){
	// return Comments.find();
	check(postId,String);
	return Comments.find({postId:postId});
});
// 发布消息
Meteor.publish('notifications',function(){
	return Notifications.find({userId:this.userId,read:false});
})