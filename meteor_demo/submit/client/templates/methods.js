/***
*	create 20151104
*
*/
Template.methods.helpers({
	// Meteor.call("upfile",a,b);
});

Template.methods.events({
	'submit form':function(e){
		e.preventDefault();		//可阻止页面刷新
		// file = $(e.target);
		// filess = $(e.target).find('form');
		// fielObj = filess[0].files;
		// console.log(document.forms.namedItem("fileinfo"))
		// console.log($("form")[0])
		// fd = new FormData(document.forms.namedItem("fileinfo"))
		// console.log(fd);

		// -----------------------------ajax
		// var xhr = new XMLHttpRequest();
		// console.log(xhr);
		// xhr.onreadystatechange = function(){
		// 	if(xhr.readyState == 4){
		// 		alert(xhr.responseText);
		// 	}
		// }

		//设置监听事件
		/*xhr.Upload.onprogress = function(evt){
			var loaded = evt.loaded;
			var total = evt.total;
			var per = Math.floor((loaded/total)*100)+"%"
			console.log(per);
		}*/
		// xhr.open('post','./abc');
		// xhr.send(fd);
		// Meteor.call("upfile",fd,function(e,r){
		// 	console.log(e+"----"+r)
		// });

		

		return false;
	}
	// ,'click #http1':function(e){

	,'submit #fileinfo':function(e){
		e.preventDefault();		//可阻止页面刷新
		
		// Meteor.call("http1","a",function(e,c){
		// 	console.log(e+'-----'+c)
		// });
		// 
		// 传统dom1
		// var xhr = new XMLHttpRequest();
		// xhr.onreadystatechange = function(){
		// 	if(xhr.readyState == 4){
		// 		alert(xhr.responseText);
		// 	}
		// }
		// xhr.open('post','./abc');
		// xhr.send(fd);
		// Meteor.call("upfile",fd,function(e,r){
		// 	console.log(e+"----"+r)
		// });
		// return false;

		// ddp = DDP.connect('http://192.168.3.104:3000');
		// console.log(ddp)
		// var file = "20150505050";
		// ddp.call('fileUpload',file,function(e,c){
		// 	console.log(e+"----"+c);
		// })

		//--------------------
		HTTP.call("POST"
			// , "http://192.168.3.139/practice/20150328/zhuce_ajax.php"
			,"http://192.168.3.139:18080/"
			// ,"http://192.168.3.139:4000"
			// ,"/abc"
			,{data: {some: "json", stuff: 1,usr:"hello world"}
				,headers:{"Access-Control-Allow-Origin":"*"}
				,params:{a:"ccc",b:"eee"}
			}
			// ,{}
			,function (error, result) {
	            if (!error) {
	              console.log("ok")
	            }
          });

		// 
		// filess = $(e.target).find('#http1');
		// 使用FormData
		var fe = document.getElementById("http1");
		var fd = new FormData(fe);
		// var fd1 = new FormData();
		// console.log(fd);
		// console.log(fd1);
		HTTP.call("POST"
			,"http://192.168.3.139:4000/"
			,{data: {some: "json", stuff: 1,usr:"hello world"}
				,headers:{"Access-Control-Allow-Origin":"*"}
				// ,params:{a:"ccc",b:"eee"}
			}
			,function (error, result) {
	            if (!error) {
	              console.log("ok")
	            }
          });



	}
})