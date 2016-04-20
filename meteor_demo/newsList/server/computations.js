Meteor.startup(function(){
// 当meteor完成加载Posts集合后只运行tracker一次
	Tracker.autorun(function(){
		// console.log('there are'+Posts.find().count() + 'posts')
		var le  = Posts.find()
		console.log(le.length)
		console.log('there are'+ 'posts')
	})
})