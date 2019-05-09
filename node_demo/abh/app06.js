// 读写excel

var fs = require('fs');
fs.readFile('abc.xlsx', function (err, data) {
   if (err) {
       return console.error(err);
   }
   console.log("异步读取: " + data.toString());
});