var express = require('express');
var mongoose = require('mongoose');

mongoose.Promise = global.Promise;
// 
mongoose.connect('mongodb://192.168.1.144:27017/Jlink2', {useNewUrlParser: true,useUnifiedTopology: true});

mongoose.connection.on('connected',function() {
    var date_string = new Date().toString();
    console.log('mongodb connection established: ' + date_string);
});

mongoose.connection.on('error',function() {
    var date_string = new Date().toString();
    console.log('mongodb error: ' + date_string + '. Closing....');
    mongoose.connection.close();
});
// console.log(mongoose)


var app = express();
app.all("*", function(req, res, next){
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "x-access-token, Origin, X-Requested-With, Content-Type, Content-Length, Accept,version, package-name");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    next();
});


app.use(express.static(__dirname + '/'));
app.get('/', function(req, res, next) {
  
  res.type('html');
  res.render('index.html');
});
app.use('/api', require('./img/api_wc_v2')());


var server = app.listen(8080, function () {
 
  var host = server.address().address
  var port = server.address().port
 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
 
})