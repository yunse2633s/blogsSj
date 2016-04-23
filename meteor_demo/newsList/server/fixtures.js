if(Posts.find().count()===0){
	// Posts.insert({
	// 	title:'Introducint Telescope'
	// 	,url:'http://sachagreif.com/'
	// });
	// Posts.insert({
	// 	title:'Meteor'
	// 	,url:'http://meteor.com'
	// });
	// Posts.insert({
	// 	title:'The Meteor Book'
	// 	,url:'http://themeteorbook.com'
	// });
	var now = new Date().getTime();
	var tomId = Meteor.users.insert({
		profile:{name:'Tom coleman'}
	});
	var tom = Meteor.users.findOne(tomId);
	var sachaId = Meteor.users.insert({
		profile:{name:'Sacha Greif'}
	});
	var sacha = Meteor.users.findOne(sachaId);
	var telescopeId=Posts.insert({
		title : 'Introducing Telescope'
		,userId:sacha._id
		,author:sacha.profile.name
		,url:'http://www.sachag.com'
		,submitted: new Date(now -7*3600*1000)
		,commentsCount:2
		,upvoters:[]
		,votes:0
	});
	Comments.insert({
		postId:telescopeId
		,userId:tom._id
		,author:tom.profile.name
		,submitted:new Date(now - 5*3600*1000)
		,body:'Interesting project sacha,can i get'
	});
	Comments.insert({
		postId:telescopeId
		,userId:sacha._id
		,author:sacha.profile.name
		,submitted:new Date(now-3*3600*1000)
		,body:'you sure can tom'
	});
	Posts.insert({
		title:'Meteor'
		,userId:tom._id
		,author:tom.profile.name
		,url:'http://meteor.com'
		,submitted:new Date(now - 10*3600*1000)
		,commentsCount:0
		,upvoters:[]
		,votes:0
	});
	for(var i=0;i<10;i++){
		Posts.insert({
			title:'循环数据' + i
			,userId:tom._id
			,author:tom.profile.name
			,url:'http://www.baidu.com'+i
			,submitted:new Date(now-12*3600*1000)
			,commentsCount:0
			,upvoters:[]
			,votes:0
		});
	}
	
}