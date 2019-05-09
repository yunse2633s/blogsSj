// 参照 https://www.cnblogs.com/imwtr/p/4398652.html，获取2018安博会厂商列表
// 
var http = require('http');
var cheerio = require('cheerio');
var fs = require("fs");
var async = require('async');
// 安博会厂商列表
var url = 'http://www.securitychina.com.cn/2018BLH/Exhibitors.asp?NF=2018&page=1&maxperpage=30';


//安博会字符集为 gb2312，需转换
var iconv = require('iconv-lite');

var result = [];

var numb = 0;
// 获取列表页中的元素组
var firstDom = function(obj){
	var $ = obj;
	// 根据class属性"body_1_left_mid_content" 搜索子节点 "li"标签
	$(".body_1_left_mid_content li").each(function(){
		// 定义空对象，用于存放一条记录
        var job = {};
        // 获取当前<li>元素中<a>标签中的"href"属性值;
        job.url = $(this).find('a').attr('href');
        // 拼接详情页的url，
        job.url = 'http://www.securitychina.com.cn' +job.url;
        // 获取<li>元素中 <a> 标签的标题
        job.name=$(this).find('a').html();
        // 进入详情页面
        httpGet(job.url, secondDom);
    });
}

// 获取第二层 元素组，并创建 cvs 文件，逐行增加
var secondDom = function(obj){
	var $ = obj;
	// 定义空数组，用于存放详情信息;
	var job = [];
	//  根据class属性"body_1_left_mid_content" 搜索子节点 "tr"标签
	$(".body_1_left_mid_content tr").each(function(){
        // 获取<tr>标签下第2条<td>标签的内容
        var item=$(this).find('td').eq(1).html();
        // 将<td>标签中的内容存入详情数组
        job.push(item);        
    });
    // 将详情数保存
    result.push(job);
}
// 链接数据库

// http.get请求 ,x是url, y是请求结束后需要执行的代码;

var httpGet=function(x, y){
	//发起 get 请求
	http.get(x, function(res){
		var chunks = [];
	    var size = 0;
	    // 监听data事件 ,并存储返回的数据
	    res.on('data',function(chunk){ 
	        chunks.push(chunk);
	        size += chunk.length;
	    });
	    // 监听end事件 ,并存储返回的数据
	    res.on('end',function(){  //数据传输完
	        var data = Buffer.concat(chunks,size);  
	        var html = iconv.decode(data,'gb2312'); 
	        var $ = cheerio.load(html, {decodeEntities: false}); 
	        y($);
	    });
	});
	
};

var newFile = function(fd){

	fs.writeFile(fd, otherMsg, 'utf8', function(err){
		if(err){
			return console.log(err)
		}
	})
}
/*
async.eachSeries([1], function(pn, cb0){
	var urlBasl = 'http://www.securitychina.com.cn/2018BLH/Exhibitors.asp?NF=2018&page='+ pn +'&maxperpage=30';
	async.waterfall([
		function(cb1){
			//获取列表页的DOM 结构
			var domNode = httpGet(urlBasl);
			cb1(null, domNode);
		}, function(dom, cb1){
			// 获取 DOM 中的元素数组
			var noteArr=[];
			cb1(null, noteArr)
		}, function(nodes, cb1){
			//循环node 获取详情
			async.eachSeries(nodes, function(node, cb2){
				//获取详情页信息
			}, cb1)
		}], cb0);
},function(err, result){
	console.log('err', err, result)
})
*/