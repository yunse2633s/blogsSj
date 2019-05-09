// 读写 csv文件
// 
var fs = require("fs");
var iconv= require('iconv-lite');

var cvsCollection;
var path = '123.csv';
//读取 123.csv文件
fs.readFile(path, function (err, data) {
    var table = new Array();
    if (err) {
        console.log(err.stack);
        return;
    }

    ConvertToTable(data, function (table) {
        console.log(table);
        cvsCollection = table;
    })
});
console.log("程序执行完毕");

function ConvertToTable(data, callBack) {
    // data = data.toString();
        	data = iconv.decode(data,'gbk'); 
    console.log('dat', data)
    var table = new Array();
    var rows = new Array();
    rows = data.split("\r\n");
    for (var i = 0; i < rows.length; i++) {
        table.push(rows[i].split(","));
    }
    callBack(table);
}

// 写入csv 文件
// 打开 open
fs.open(path, 'a+', function(err, fd){
	if(err){
		return console.log(err);
	}
	var otherMsg = '\r\n德国,慕尼黑, 4';
	otherMsg = iconv.encode(otherMsg, 'GBK');
	//a+追加写
	// 判断 文件最后一行是否有\r\n
	fs.writeFile(fd, otherMsg, 'utf8', function(err){
		if(err){
			return console.log(err)
		}
	})
} )