var postsData=[
	{
		title:'Introducing Telescope',
		url:'http://sachagref.com'
	},
	{
		title:'Meteor'
		,url:'http://meteor.com'
	}
	,{
		title:'The Meteor Book'
		,url:'http://themeteorbook.com'
	}
];

Template.postsList.helpers({
	posts:postsData
});