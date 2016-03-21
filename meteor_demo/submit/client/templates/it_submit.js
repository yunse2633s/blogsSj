Template.itSubmit.events({
	'submit form':function(e){
		e.preventDefault();		//可阻止页面刷新
		file = $(e.target);
		filess = $(e.target).find('#File')
		fielObj = filess[0].files[0];
		console.log(filess[0].files[0])
		// console.log(file)
		var it={
			name:$(e.target).find('[name=name]').val(),
			pwd:$(e.target).find('[name=pwd]').val()
		};
		it._id = Its.insert(it);	//插入成功后，将记录的id返回
		console.log(it._id);
		// console.log(it._id);
		// Router.go('otherpage',post);		// 指定提交后跳转的页面
		// 上传图片
		// HTTP.call("POST", "http://192.168.8.139/php/demo4.php",
  //         {data: {some: "json", stuff: 1}},
  //         function (error, result) {
  //           if (!error) {
  //             Session.set("twizzled", true);
  //           }
  //         });
// 		var form = $(e.target).find("form")
// 		var oMyForm = new FormData();
//  
// 		oMyForm.append("username", "Groucho");
		// oMyForm.append("accountnum", 123456); // 数字123456被立即转换成字符串"123456"
		 
		// fileInputElement中已经包含了用户所选择的文件
		// oMyForm.append("userfile", fileInputElement.files[0]);
		//  oMyForm.append("userfile", filess[0].files[0]);
		// oMyForm.append("Access-Control-Allow-Origin", "*");
		// var oFileBody = "<a id='a'><b id='b'>hey!</b></a>"; // Blob对象包含的文件内容
		// var oBlob = new Blob([oFileBody], { type: "text/xml"});
		//  
		// oMyForm.append("webmasterfile", oBlob);

		// var oReq = new XMLHttpRequest();
		// oReq.open("POST", "http://192.168.3.139:18080/upload");
		// oReq.send(oMyForm);

	},
	'click button':function(e){
		// e.preventDefault();

		// ids = Its.find({},{"_id":1}).fetch();
		// for(var i in ids){
		// 	console.log(ids[i]._id)
		// 	console.log(Its.remove(ids[i]._id))
		
		var filedata = new FormData;

	
	}
});

Template.view.helpers({
	views:function(){
		return Its.find();
	},
	keystatus:function(){
		return Session.get('isKeyboardVisible');
	}
});