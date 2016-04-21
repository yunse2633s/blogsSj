Meteor.publish('posts',function(){
	return Posts.find();
	// 查询flagged字段为false的记录
	// return Posts.find({flagged:false})
	// Posts.find({flagged:false,author:author})
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

Meteor.publish('comments',function(postId){
	// return Comments.find();
	check(postId,String);
	return Comments.find({postId:postId});
});