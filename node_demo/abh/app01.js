// 获取安博会的企业名录
// http://www.securitychina.com.cn/2018BLH/Exhibitors.asp?NF=2018&page=1&maxperpage=30
// 页面代码是 gb2312 , 需要使用iconv 转码


var http = require('http');
var iconv = require('iconv-lite')

// var url = "http://www.securitychina.com.cn/2018BLH/Exhibitors.asp?NF=2018&page=1&maxperpage=30";
// var url = "http://www.baidu.com"
var url = "http://www.securitychina.com.cn";
http.get(url, function(res){
	var length=0;
    var arr=[];
    res.on("data",function(chunk){
        arr.push(chunk);
        length+=chunk.length;
    });   
    res.on("end",function(){
        var data=Buffer.concat(arr,length);
        // 由于nodejs默认的编码方式是utf-8，需要将原始的二进制码流按照网页原来的编码方式解码，则不会出现乱码。 
        var change_data = iconv.decode(data,'gb2312'); 
        console.log(change_data);
        // 获取<li>标签内容
        	// 获取<li>标签下 <a>标签，
        		// 获取href的内容
        	// 获取<li>标签下的image 标题，获取 src
        	// 
    }) 

}).on('error', function(err){
	console.log('err', err)
})
