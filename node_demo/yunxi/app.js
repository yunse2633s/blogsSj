

var express = require('express');
var https = require('https');
var fs = require('fs');
var path = require('path');


// var app = express();

// app.get('/',function(req,res) {
    
//         res.send({status:'success',msg:'Welcome to the TRAFFIC module of RSC system.'});

// });

// app.use('*',function(req, res) {
//     res.send({status:'not_found'});
// });

// app.listen('8888', function(err) {
//     console.log('=================================================');
//     if(err) {
//         console.log('Error Occurred When Starting Server, ' + new Date().toString());
//     } else {

//         console.log('Server Started. ' + new Date().toString());
//         console.log('===================config========================');
//     }
// });
// 
var tspath='yunqilive.xiaozhizuo.tv_mayi_logo_yq1080p-1537324518894.ts';
var checkCodeUrl = 'https://yunqilive.xiaozhizuo.tv/yunqi/'+ tspath;
/*
 ts: https://yunqilive.xiaozhizuo.tv/yunqi/yunqilive.xiaozhizuo.tv_mayi_logo_yq1080p-1537324518894.ts
`
 vod
`
 todo: https://dno-901-2018yq-hd.youku.com/2018yq/mainforumlogo_yq1080p.m3u8
    `

#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:1358
#EXT-X-TARGETDURATION:8
#EXTINF:8.000,
dno-901-2018yq-hd.youku.com_mainforumlogo_yq1080p-1537324904330.ts
#EXTINF:8.000,
dno-901-2018yq-hd.youku.com_mainforumlogo_yq1080p-1537324912326.ts
#EXTINF:8.000,
dno-901-2018yq-hd.youku.com_mainforumlogo_yq1080p-1537324920336.ts

    `


 */
var ccc = function(){
    var filePath = path.normalize(__dirname + '/tmp' + tspath);

    fs.exists(filePath, function(exists){
        if(exists){
            console.log('cunzai', filePath);
        }else{
            console.log('checkCodeUrl', checkCodeUrl)
            https.get(checkCodeUrl,function(res){
                console.log('res', res)
                var datas = [];
                var size = 0;
                res.on('data', function(data){
                    datas.push(data);
                    size += data.length;
                })
                res.on('end', function(data){
                    var buff = Buffer.concat(datas, size);
                    // var pic = buff.toString('base64');
                    fs.writeFileSync(filePath, datas);
                    console.log('ok')
                    // callback({success:true, data:pic});
                })
            }).on('error',function(err){
                console.log('err', err)
                // callback({success:false, msg:'获取验证码失败'});
            })

            //
            // var request = http.request(options, function(res) {
            //     var chunks = [];
            //     res.on("data", function (chunk) {
            //         chunks.push(chunk);   // 获取到的音频文件数据暂存到chunks里面
            //     });

            //     res.on("end", function () {
            //         var body = Buffer.concat(chunks);
            //         fs.writeFileSync(filePath, body);
            //         cb(null, data.order_id +'.mp3');
            //     });
            // });
            // request.on('error', function(e) {
            //     return cb(e.message);
            // });
            // request.write(postData);
            // request.end();
        }
    });
}
var bbb= function(){
    var ary = [];
    https.get('https://yunqilive.xiaozhizuo.tv/yunqi/yqtv_logo_yq1080p.m3u8', function(res){
            var datas = [];
            var size = 0;
            res.on('data', function(data){
                datas.push(data);
                size += data.length;
            })
            res.on('end', function(data){
                var buff = Buffer.concat(datas, size);
                buff= buff.toString();
                /*
                // 正则和字符串替换.
                var _tmp = buff.split(/\n/);
                for(var i=0; i<_tmp.length; i++){
                    if(_tmp[i].indexOf('.ts') != -1){
                        ary.push(_tmp[i]);
                    }
                }
                */
               // var _tmp=buff.split(/([a-z][A-Z][0-9])(ts\n)$/);
               var _tmp=buff.split(/\n(.*)\.ts/);
                console.log('ok',_tmp)
            })
        }).on('error',function(err){
            console.log('err', err)
        })

}

bbb();