Meteor.methods({
    test: function (a,b) {
        console.log(a+"----"+b); 		//服务端输出
        var datatime= new Date();
        return datatime+"--from server result";
    }
    ,http1:function(e){

    	HTTP.call("POST"
			// , "http://192.168.3.139/practice/20150328/zhuce_ajax.php"
			,"http://192.168.3.139:18080/"
			// ,"/abc"
			,{data: {some: "json", stuff: 1},headers:{"Access-Control-Allow-Origin":"*"}}
			// ,{}
			,function (error, result) {
	            if (!error) {
	              console.log("ok")
	            }
          });
    	// return "ok23423423423";
    }
});

// var formidable = Npm.require('formidable');

// formidable = Npm.require('formidable');
 // var    fs = Npm.require('fs');
 