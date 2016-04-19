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
		// 安全性检查
		console.log('-',check)
		check(123,String);
		check(postAttributes,{
			title:String
			,url:String
		})
		// 防止重复发送
		console.log(postAttributes)
		var postWithSameLink=Posts.findOne({url:postAttributes.url})
		if(postWithSameLink){
			console.log('重复了')
			return {
				postExists:true,
				_id:postWithSameLink._id
			}
		}
		console.log('重复了就不继续了')
		var user=Meteor.user(); //获取用户信息
		// _.extend()方法来源于underscore库
		var post=_.extend(postAttributes,{
			userId:user._id
			,author:user.username
			,submitted:new Date()
		})
		// 插入数据并返回记录_id
		var postId=Posts.insert(post)
		return {
			_id:postId
		}
	}
})