Template.abc.helpers({
	data:function(){
	return "返回值";
	}
});

Template.abc.onRendered(function(){
	// var form = new formidable.IncomingForm();   //创建上传表单
	// console.log(formidable)
	
	console.log( "自刷新")
});
Template.abc.onCreated(function(){
	console.log("onCreated")
})