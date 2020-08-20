//外部工具引用
var async = require('async');
var express = require('express');
var mongoose = require('mongoose');
var _ = require('underscore');
var cf=require('./config');

var Schema=mongoose.Schema;
// 声明表结构
// 刷卡记录
var recordSchema=new Schema({
    '_id':{type:Number}
    ,'dev_sno':{type: String}
    ,'device_type':{type: Number}
    ,'person_id':{type: Number}
    ,'person_type':{type: String}
    ,'personName':{type: String}
    ,'updateTime':{type: Number}
    ,'deviceName':{type: String}
    ,'captureImg':{type: String}
},{collection:'record'})
// 设备
var deviceSchema=new Schema({
    'dev_sno':{type: String}
    ,'name':{type: String}
    ,'throughType':{type: String}
    ,'deleteTime':{type:Number}
},{collection:'device'})
// 人员
var staffSchema=new Schema({
    '_id':{type:Number}
    ,'name':{type:String}
    ,'department':{type:Number}
    ,'deleteTime':{type:Number}
    ,'showImg':{type:String}
},{collection:'staff'})

// 部门下的角色id,通过角色id 查部门
var departmentSchema=new Schema({
    '_id':{type:Number}
    ,'name': {type:String}   
    ,'parentId':{type:Number}
    ,'deleteTime':{type:Number}
},{collection:'department'})

//表的实例化

// 访客表
var record=mongoose.model('record', recordSchema)

// 设备
var device=mongoose.model('device', deviceSchema)

//人员
var staff=mongoose.model('staff', staffSchema)

//部门
var department=mongoose.model('department', departmentSchema) 


// 初始时间段
var timeArr=function(nowt){
    dat_str=nowt.toLocaleDateString()
    day_start=new Date(dat_str).getTime()
    time_arr=[]
    oneTime=60*60*1000
    for(var i=0; i<=24; i++){
        vt=day_start+oneTime*i;
        time_arr.push(vt)
    }
    return time_arr
}
// 初始化结果
var v_data=JSON.parse(JSON.stringify(cf.v_data)),
updateTime=0,
updateDate=1;

/**
 计算每个时段的 进出
 */
var nowStream=function(timearr,i,arm,cb){
    record.aggregate([
        {'$match':{updateTime: { '$gte': timearr[i], '$lt': timearr[i+1] },'person_type': '4',}}, 
        {'$group' : {'_id' : '$person_id', 'updateTime' : {'$first' : "$updateTime"},'dev_sno' : {'$first' : "$dev_sno"}}}
        ,{$lookup:{
             from: "device",
             localField: "dev_sno",
             foreignField: "dev_sno",
             as: "device_info"
        }}
        ,{$project:{'_id':1,'dev_sno':1,"device_info.throughType":1}}
    ]).exec(function(x,y){
        // console.log('y',y)
        co = _.countBy(y, function(num) {
            // console.log('num',num['_id'],num['device_info'][0])
          return num['device_info'][0] && num['device_info'][0]['throughType']=='in' ? 'in': 'out';
        });
        v_data['transit_trend'][arm]['out_count']=co['out'] || 0
        v_data['transit_trend'][arm]['enter_count']=co['in'] || 0
        cb()
        
    })
}
// var nowtime=new Date('2020/07/28 18:00:00')
var nowtime=new Date()

var timeStream=function(nowt, x){
    time_arr=timeArr(nowt)
    nowdate=nowtime.getDate(),
    nowhour=nowtime.getHours(),
    updateTime=nowhour-1,
    updateDate=nowdate;
    console.log('updateTime:',updateTime,',updateDate:',updateDate)
    //统计之前时段的数据
    for(var i=0; i<updateTime; i++){
        (function(arm){
            nowStream(time_arr,i,arm,function(){})
        })(i)
    }
    x()
}
//第一次运行时预设值
timeStream(nowtime, function(){

})


// 如果记录表中有人员，进出、公司名、时段等。 做统计的时候，就不用再进行关联查询了

module.exports = function() {
    var api = express.Router();
    api.get('/labor_transit_statistics', function (req, res, next) {
        // 设备表，公司表，人员表
        var devices={}, departps={}, work_info={}, user_info={}, device_info={};
        runtime=new Date()
        run_t1=runtime.getTime()
        runhours=runtime.getHours()
        rundate=runtime.getDate()
        async.waterfall([
            function(cb){
                //日期改变或时间间隔，初始化数据
                if(rundate != updateDate || runhours > updateTime+2){
                    v_data=JSON.parse(JSON.stringify(cf.v_data))
                    timeStream(runtime,cb)
                }else{
                    nowStream(time_arr,runhours,runhours,cb)
                }

            },
            function(cb){
                // 获取设备目录
                device.find({'deleteTime':0},['dev_sno', 'throughType', 'name'],function(err, result){
                    devices_in=[]
                    devices_out=[]
                    devices_both=[]
                    device_info=_.indexBy(result, 'dev_sno')
                    _.each(result, function(x){
                        switch(x['throughType']){
                            case 'in':
                                devices_in.push(x.dev_sno);
                                break;
                            case 'out':
                                devices_out.push(x.dev_sno);
                                break;
                            default:
                                devices_both.push(x.dev_sno);
                        }
                    })           
                    cb(err, {'in':devices_in, 'out': devices_out, 'both': devices_both})
                })
            }, 
            function(deviceR, cb){
                devices=deviceR
                // 获取公司名录
                department.find({'parentId':{'$gte':1}, 'deleteTime':0})
                .sort({'parentId':1})
                .select('name _id parentId')
                .exec(function(err, result){
                    work_info=_.indexBy(result,'_id'); //公司职务目录
                    departp={}
                    _.each(result, function(x){
                        if(x.parentId==1){
                            x=x.toObject()
                            x['child']=[]
                            departp[x._id]=x
                        }else{
                            departp[x.parentId]['child'].push(x._id)
                        }
                    })

                    cb(err, departp)

                    })
            }, 
            function(departmentR, cb){
                departps=departmentR
                // 获取公司名下人员,department排序
                staff.find({'deleteTime':0}).sort({'department':1}).select('_id department showImg').exec(function(err, result){

                    //获取用户数
                    v_data['total_count']=result.length
                    usertp={}
                    user_info=_.indexBy(result, '_id')
                    _.each(result, function(x){
                        if(usertp.hasOwnProperty(x['department'])){
                            usertp[x.department].push(x['_id'])
                        }else{
                            usertp[x.department]=[x['_id']]
                        }
                    })
                    
                    // 将用户放入公司组下
                    _.each(departps, function(x){
                        x['user']=[]
                        // 循环部门中的职位
                        _.each(x.child, function(y){
                            x['user']=_.union(x['user'],usertp[y])
                            x['user_count']=x['user'].length
                        })
                    })
                   cb(err, departps) 
                })

            },
            function(staffR, cb){
                //获取当天，进出人总数
                async.parallel([
                    function(cpp){
                        record.aggregate([
                            {'$match':{'dev_sno':{'$in': devices['in']}, 'updateTime': { '$gte': time_arr[0], '$lt': time_arr[24] },'person_type': '4'}}, 
                            {'$group' : {'_id' : '$person_id'}}
                            ])
                        .exec(function(x,y){
                            v_data['entry_count']=y.length
                            cpp(x,y)
                        })
                    }, function(cpp){
                        record.aggregate([
                            {'$match':{'dev_sno':{'$in': devices['out']}, 'updateTime': { '$gte': time_arr[0], '$lt': time_arr[24] },'person_type': '4'}}, 
                            {'$group' : {'_id' : '$person_id'}}
                            ])
                        .exec(function(x,y){
                            v_data['out_count']=y.length
                            cpp(x,y)
                        })
                    }],cb)
            }, function(onlyperson, cb){
                // 统计每家单位的进场的人数
                var p_in_id=_.pluck(onlyperson[0],'_id')
                v_data['real_count']= v_data['entry_count']-v_data['out_count']
                //计算每个公司的 现场人数
                tmp_company=[]
                _.each(departps, function(x){
                    tmp_company.push({
                        "total_labor": x['user_count'],
                        "unit": x['name'],
                        "enter_labor": _.intersection(x.user, p_in_id).length //计算交集数
                    })
                })
                tmp_company=_.sortBy(tmp_company, "enter_labor")
                tmp_company_a=[]
                // 降序排列
                _.each(tmp_company, function(x){ tmp_company_a.unshift(x)})
                v_data['companys']=tmp_company_a
                
                record.find({'person_type':'4'})
                    .select('_id person_id personName captureImg updateTime dev_sno')
                    .sort({'updateTime':-1})
                    .limit(1)
                    .exec(cb)
            }], function(err, time_user){
                v_data['user_info']={
                        "sign_time": new Date(time_user[0]['updateTime']).toLocaleString(),
                        "direction":  device_info[time_user[0]['dev_sno']]['throughType'] == 'in' ? '进入': '外出' ,
                        "name": time_user[0]['personName'],
                        "work_type": work_info[user_info[time_user[0]['person_id']]['department']]['name'],
                        "device_name": device_info[time_user[0]['dev_sno']]['name'] ,
                        "sign_avatar": cf.imgurl + time_user[0]['captureImg'],
                        "avatar": cf.imgurl + user_info[time_user[0]['person_id']]['showImg'],
                        "unit": departps[work_info[user_info[time_user[0]['person_id']]['department']]['parentId']]['name']
                    }
                run_t2=new Date().getTime()
                console.log('耗时：', (run_t2-run_t1))
                e={
                    "msg": "成功",
                    "code": 200,
                    "data": v_data
                    ,"status": 'success'
                };
                res.send(e)
        })
    });


    return api;
};