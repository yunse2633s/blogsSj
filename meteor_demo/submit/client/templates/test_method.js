/**
*	
*/
Template.method.helpers({
	result:function(){
		// return "ok"
		var a="hong",b="ceshi";
		Meteor.call('test',a,b,function(error,result){
			console.log(result);

		})
	}
});
