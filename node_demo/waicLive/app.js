/*
 * 2020 07/09 - 07/11 
 * @type {[type]}
 * 1. 获取m3u8的列表
 * 2. 获取ts文件
 * 3. 压缩合并ts文件
 *
 * quest:
 * 长时间运行
 * forever
 * pm2
 * nohup 
 */
var express = require('express');
var https = require('https');
var fs = require('fs');
var path = require('path');
var async = require('async');

//  2019 9.25 
//  
//  获取视频目录
g_mulu='https://1252524126.vod2.com/9764a7a5vodtransgzp1252524126/f180ef2a5285890805036424574/v.f230.m3u8'



url2='https://'+g_mulu.split('/')[2] + '/'   //https://livevideo.cbndata.com/';
url3= g_mulu.split('/')[3] + '/'   //'caster/';
//url3='9764a7a5vodtransgzp1252524126/f180ef2a5285890805036424574/'
url4=''; //来自m3u8目录中的数组

var downFlag = false;
var downUrl = '';
var downFileName = '';
docfilename=new Date().toLocaleDateString().replace(/-/g,'') + 'a' //toLocaleString()


/**
 * 下载开始
 */
function startDownloadTask (imgSrc, dirName,fileName, cb) {
    var req = https.request(imgSrc, function(res) {
        var out = fs.createWriteStream(dirName + "/" + fileName);
        res.on('data', function (chunk) {
            //写文件
            out.write(chunk, function () {
            });
            
        });
        res.on('end', function() {
            downFlag = false;
            console.log("end downloading " + imgSrc);
            cb(null, null)
            
        });
    });
    req.on('error', function(e){
        console.log("request " + imgSrc + " error, try again");
        cb(e)
    });
    req.end();
}
time =new Date().getTime();
t2=new Date().getTime() //'2020-07-09 16:30:00'

//创建文件夹
// 设置结束时间



async.waterfall([

        function (cb) {
            var ary = [];
            https.get(g_mulu, function(res){
                var datas = [];
                var size = 0;
                res.on('data', function(data){
                    datas.push(data);
                    size += data.length;
                })
                res.on('end', function(data){
                    var buff = Buffer.concat(datas, size);
                    buff= buff.toString();
                    console.log('000')
                    var _tmp=buff.split(',')
                    _tmp.forEach(function(x,y){
                        if(x.indexOf('.ts')>0){
                            ary.push(x.split('\n')[1])
                        }
                    })
                    cb(null, ary)
                })
            }).on('error',function(err){
                cb(err)
            })
        }, 

        function (plans, cb) {
            console.log(plans)
            //var ipc=1
            async.eachSeries(plans, function (plan, cb1) {
                console.log('plan', plan)
                console.log()
                filename=plan.split('?')[0].split('.ts')[0];
                console.log('filename',filename)
                var filePath = path.normalize(__dirname + '/tmp/'+docfilename +'/'+ filename+'.ts');
                var checkCodeUrl=url2+url3+plan;
                var fp1 = path.normalize(__dirname + '/tmp/'+docfilename)
                var fp2 = filename +'.ts'
                //var fp2 = filename + ipc +'.ts'
                //ipc+=1
                fs.exists(filePath, function(exists){
                    if(exists){
                        console.log('cunzai', filePath);
                        cb1()
                    }else{
                        startDownloadTask(checkCodeUrl,fp1, fp2, cb1);
                    }})
                
                }, cb)
        }], function(err, result){
            console.log('---1',err, result)
    })

