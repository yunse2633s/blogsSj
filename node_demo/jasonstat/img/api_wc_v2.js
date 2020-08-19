//外部工具引用
var async = require('async');
var express = require('express');
var mongoose = require('mongoose');
var _ = require('underscore');

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


// 获取当天的开始和结束时间，时间点
dat_str=new Date().toLocaleDateString()
day_start=new Date(dat_str).getTime()
time_arr=[]
oneTime=60*60*1000
for(var i=0; i<=24; i++){
    vt=day_start+oneTime*i;
    time_arr.push(vt)
}
// 初始化结果
var v_data ={
        "user_info": {
            "sign_time": "",
            "direction": "",
            "name": "",
            "work_type": "",
            "device_name": "",
            "sign_avatar": "",
            "avatar": "",
            "unit": ""
        },
        "updateTime": 0,
        "transit_trend": [
            {
                "h": "0",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "1",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "2",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "3",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "4",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "5",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "6",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "7",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "8",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "9",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "10",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "11",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "12",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "13",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "14",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "15",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "16",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "17",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "18",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "19",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "20",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "21",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "22",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "23",
                "enter_count": "0",
                "out_count": "0"
            }
        ],
        "total_count": "0",
        "out_count": "0",
        "entry_count": "0",
        "real_count": "0",
        "companys": [
        ]
    }

/**
 计算每个时段的 进出
 */

//什么情况获取新数据， 更新时间与当前时间相隔小于2时，如果当前时间 大于更新时间，则从循环更新时间到当前时间, 


var timeStream=function(x){
    nowhour= new Date().getHours()
    if(v_data['updateTime']>=nowhour-1){
        return false
    }
    for(var i=v_data['updateTime']; i<nowhour+1; i++){
        console.log('i', i);
        (function(arm){
            console.log({ '$gte': time_arr[i], '$lt': time_arr[i+1] })
            record.aggregate([
                {'$match':{updateTime: { '$gte': time_arr[i], '$lt': time_arr[i+1] },'person_type': '4',}}, 
                {'$group' : {'_id' : '$person_id', 'updateTime' : {'$first' : "$updateTime"},'dev_sno' : {'$first' : "$dev_sno"}}}
                ,{$lookup:{
                     from: "device",
                     localField: "dev_sno",
                     foreignField: "dev_sno",
                     as: "device_info"
                }}
                ,{$project:{'_id':1,'dev_sno':1,"device_info.throughType":1}}
            ]).exec(function(x,y){
                co = _.countBy(y, function(num) {
                  return num['device_info'][0]['throughType']=='in' ? 'in': 'out';
                });
                v_data['transit_trend'][arm]['out_count']=co['out']
                v_data['transit_trend'][arm]['enter_count']=co['in']
            })

        })(i)
    }
    //执行之后，更新时间改为当前时间-1
    v_data['updateTime']=nowhour-1
    x()
}
    
timeStream(function(){})

// 如果记录表中有人员，进出、公司名、时段等。 做统计的时候，就不用再进行关联查询了

module.exports = function() {
    var api = express.Router();
    api.get('/labor_transit_statistics', function (req, res, next) {
        // 设备表，公司表，人员表
        var devices={}, departps={}, work_info={}, user_info={}, device_info={};
        
        run_t1=new Date().getTime()
        async.waterfall([
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
                record.count({updateTime: { '$gte': time_arr[0], '$lt': time_arr[24] },'person_type': '4', dev_sno: {'$in':devices['in']} })
                .exec(function(err, p_in){
                  v_data['entry_count']=p_in
                  record.count({'updateTime': { '$gte': time_arr[0], '$lt': time_arr[24] },'person_type': '4','dev_sno':{'$in':devices['out']} })
                  .exec(function(err, p_out){
                        v_data['out_count']=p_out
                        cb(err, p_out)
                    })
                })


            }, function(onlyperson, cb){
                // 统计每家单位的现场人数
                record.aggregate([
                    {'$match':{updateTime: { '$gte': time_arr[0], '$lte': time_arr[24] },'person_type': '4'}}, 
                    {'$group' : {'_id' : '$person_id', 'updateTime' : {'$first' : "$updateTime"},'dev_sno' : {'$first' : "$dev_sno"}}}
                    ,{$lookup:{
                         from: "device",
                         localField: "dev_sno",
                         foreignField: "dev_sno",
                         as: "device_info"
                    }}
                    ,{$project:{'_id':1,'dev_sno':1,"device_info.throughType":1}}
                ])
                .exec(function(e,x){
                    var p_in=_.filter(x, function(i){ return i['device_info'][0]['throughType']=='in';})
                    var p_out=_.filter(x, function(i){ return i['device_info'][0]['throughType']=='out';})
                    var p_in_id=_.pluck(p_in,'_id')
                    v_data['real_count']=p_in.length
                    //计算每个公司的 现场人数
                    tmp_company=[]
                    _.each(departps, function(x){
                        tmp_company.push({
                            "total_labor": x['user_count'],
                            "unit": x['name'],
                            "enter_labor": _.intersection(x.user, p_in_id).length
                        })
                    })
                    tmp_company=_.sortBy(tmp_company, "enter_labor")
                    tmp_company_a=[]
                    // 降序排列
                    _.each(tmp_company, function(x){ tmp_company_a.unshift(x)})
                    v_data['companys']=tmp_company_a
                    cb()                     
                    //如何计算进出次数，一分钟进2次怎么计算 存在被删除人员没有同步到硬件设备上
                })
            }, function(cb){
                // 获取最新进入的人,及人员信息
                // 已知设备组，公司组，人员组，通过record获取相关的信息， 单独查一下人员图片
                tc=new Date().getTime()
                async.waterfall([
                function(cb2){
                    record.find({'person_type':'4'})
                    .select('_id person_id personName captureImg updateTime dev_sno')
                    .sort({'updateTime':-1})
                    .limit(1)
                    .exec(cb2)
                },function(time_user, cb2){
                    
                    v_data['user_info']={
                        "sign_time": new Date(time_user[0]['updateTime']).toLocaleDateString(),
                        "direction":  device_info[time_user[0]['dev_sno']]['throughType'] == 'in' ? '进入': '外出' ,
                        "name": time_user[0]['personName'],
                        "work_type": work_info[user_info[time_user[0]['person_id']]['department']]['name'],
                        "device_name": device_info[time_user[0]['dev_sno']]['name'] ,
                        "sign_avatar": 'http://192.168.1.144/' + time_user[0]['captureImg'],
                        "avatar": 'http://192.168.1.144/' + user_info[time_user[0]['person_id']]['showImg'],
                        "unit": departps[work_info[user_info[time_user[0]['person_id']]['department']]['parentId']]['name']
                    }
                    cb2()
                }],cb)
            }], function(err, result){
                run_t2=new Date().getTime()
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