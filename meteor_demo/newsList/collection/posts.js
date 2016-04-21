Posts = new Mongo.Collection('posts')
// Post.insert() ,Post.update()
// 仅限登录者可以发布帖子
// 移除insecure包(恢复数据安全)
// meteor remove insecure
// Posts.allow({
// 	insert:function(userId,doc){
// 		return !!userId
// 	}
// })
// 在提交页中使用Meteor.call调用postInsert方法
Meteor.methods({
	postInsert:function(postAttributes){
		console.log(postAttributes)
		// 安全性检查
		check(this.userId,String);
		check(postAttributes,{
			title:String
			,url:String
		});
		var errors = validatePost(postAttributes)
		if(errors.title || errors.url)
			throw new Meteor.Error('invalit-post',"你必须填写内容")
		// 对比延迟补偿的效果
		if(Meteor.isServer){
			postAttributes.title +="(server)";
			Meteor._sleepForMs(5000);
		}else{
			postAttributes.title +="(client)"
		}
		// 防止重复发送
		var postWithSameLink=Posts.findOne({url:postAttributes.url})
		if(postWithSameLink){
			return {
				postExists:true,
				_id:postWithSameLink._id
			}
		}
		var user=Meteor.user(); //获取用户信息
		// _.extend()方法来源于underscore库
		var post=_.extend(postAttributes,{
			userId:user._id
			,author:user.username
			,submitted:new Date()
			,commentsCount:0
		})
		// 插入数据并返回记录_id
		var postId=Posts.insert(post)
		return {
			_id:postId
		}
	}
});

Posts.allow({
	update:function(userId,post){
		return ownsDocument(userId,post);
	}
	,remove:function(userId,post){
		return ownsDocument(userId,post);
	}
});
Posts.deny({
	update:function(userId,post,fieldNames){
		// _.without(array, *values) 返回一个删除所有values值后的 array副本。
		
		return (_.without(fieldNames,'url','title').length>0)
	}
});
// 9.错误，监控posts对象
validatePost = function(post){
	var errors={};
	if(!post.title)
		errors.title="请填写标题";
	if(!post.url)
		errors.url="请填写url";
	return errors;
}
Posts.deny({
	update:function(userId,post,fieldNames,modifier){
		console.log('modifier',modifier)
		var errors = validatePost(modifier.$set);
		return errors.title || errors.url;
	}
})