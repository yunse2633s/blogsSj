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
			,upvoters:[]
			,votes:0
		})
		// 插入数据并返回记录_id
		var postId=Posts.insert(post)
		return {
			_id:postId
		}
	}
	,upvote:function(postId){
		check(this.userId,String);
		check(postId,String);
		// var post = Posts.findOne(postId);
		// if(!post){
		// 	throw new Meteor.Error('无效','记录没找到');
		// }
		// if(_.include(post.upvoters,this.userId)){
		// 	throw new Meteor.Error('无效','已经发')
		// }
		// Posts.update(post._id,{
		// 	$addToSet:{upvoters:this.userId}
		// 	,$inc:{votes:1}
		// })
		// 两次调用数据库效率低，引入极速状态 $ne 不等于
		var affected = Posts.update({
				_id:postId
				,upvoters:{$ne:this.userId}
			}
			,{
				$addToSet:{upvoters:this.userId}
				,$inc:{votes:1}
			});
		if(!affected){
			throw new Meteor.Error('无效','不能对它投票')
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
		console.log('服务端更新拒绝',fieldNames,_.without(fieldNames,'url','title'))
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