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
dat_str=new Date('2020-07-29').toLocaleDateString()
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
            "sign_time": "--时间",
            "direction": "--方向",
            "name": "--姓名",
            "work_type": "--岗位",
            "device_name": "--通道",
            "sign_avatar": "现场照",
            "avatar": "证件照",
            "unit": "jason"
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
                "enter_count": "10",
                "out_count": "20"
            },
            {
                "h": "2",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "3",
                "enter_count": "30",
                "out_count": "40"
            },
            {
                "h": "4",
                "enter_count": "0",
                "out_count": "0"
            },
            {
                "h": "5",
                "enter_count": "50",
                "out_count": "60"
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


// var ccc = function(t1, t2,cb){
//     return record.aggregate([
//             {'$match':{updateTime: { '$gte': t1, '$lt': t2 },'person_type': '4',}}, 
//             {'$group' : {'_id' : '$person_id', 'updateTime' : {'$first' : "$updateTime"},'dev_sno' : {'$first' : "$dev_sno"}}}
//             ,{$lookup:{
//                  from: "device",
//                  localField: "dev_sno",
//                  foreignField: "dev_sno",
//                  as: "device_info"
//             }}
//             ,{$project:{'_id':1,'dev_sno':1,"device_info.throughType":1}}
//         ]).exec(cb)
// }
// 获取 全天的进出数/ 另外一个算法，用进出的设备集对比数量
// record.aggregate([
//         {'$match':{updateTime: { '$gte': time_arr[0], '$lt': time_arr[24] },'person_type': '4'}}, 
//         {'$group' : {'_id' :{'cid':'$_id', 'person_id': '$person_id', 'updateTime':'$updateTime'}, 'dev_sno' : {'$first' : "$dev_sno"}} }
//         ,{$lookup:{
//              from: "device",
//              localField: "dev_sno",
//              foreignField: "dev_sno",
//              as: "device_info"
//         }}
//         ,{$project:{'_id':1,'dev_sno':1,"device_info.throughType":1}}
//     ]).exec(function(x,y){

//         var p_in=_.filter(y, function(i){ return i['device_info'][0]['throughType']=='in';})
//         var p_out=_.filter(y, function(i){ return i['device_info'][0]['throughType']=='out';})
//         var p_both=_.filter(y, function(i){ return i['device_info'][0]['throughType']=='both';})
//         v_data['out_count']=p_out.length
//         v_data['entry_count']=p_in.length
//         console.log('dev_sno',y.length, p_in.length,  p_out.length, p_both.length)
//     })

/**
 计算每个时段的 进出
 */

// console.log("v_data['updateTime']" , v_data['updateTime'], nowhour)
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
                console.log('arm', arm, y.length)

                var p_in=_.filter(y, function(i){ return i['device_info'][0]['throughType']=='in';})
                var p_out=_.filter(y, function(i){ return i['device_info'][0]['throughType']=='out';})
                // console.log('ccc', new Date(time_arr[arm]).getHours(), p_in.length, p_out.length)
                v_data['transit_trend'][arm]['out_count']=p_out.length
                v_data['transit_trend'][arm]['enter_count']=p_in.length
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
        var devices={}, departps={}, users={};
        run_t1=new Date().getTime()
        async.waterfall([
            function(cb){
                    // 获取设备目录
                    device.find({'deleteTime':0},['dev_sno', 'throughType', 'name'],function(err, result){
                        devices_in=[]
                        devices_out=[]
                        devices_both=[]
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
                    users=result
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
                        // console.log('p_in', p_in, p_out)
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
                    // onlyperson去重后人数718条, count 有1408条 aggregate有718条，628条进，52条出，剩余是both 38
                    var p_in_id=_.pluck(p_in,'_id')
                    v_data['real_count']=p_in.length
                    // console.log('现场人数', p_in.length,'现场离开', p_out.length)
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
                    // console.log(_.difference(p_in_id, weihe_c))
                })
            }, function(cb){
                // 获取最新进入的人,及人员信息
                // 已知设备组，公司组，人员组，通过record获取相关的信息， 单独查一下人员图片
                // console.log(devices, departps, users)
                tc=new Date().getTime()
                async.waterfall([
                function(cb2){
                    record.find({'person_type':'4'})
                    .select('_id person_id personName captureImg updateTime')
                    .sort({'updateTime':-1})
                    .limit(1)
                    .exec(cb2)
                },function(time_user, cb2){
                    console.log(time_user[0])
                    record.aggregate([
                        {'$match':{'_id': time_user[0]['_id']}}, 
                        {'$group' : {'_id' : '$_id', 'person_id' : {'$first' : "$person_id"},'dev_sno' : {'$first' : "$dev_sno"}}}
                        ,{$lookup:{
                             from: "device",
                             localField: "dev_sno",
                             foreignField: "dev_sno",
                             as: "device_info"
                        }}                    
                        ,{$lookup:{
                             from: "staff",
                             localField: "person_id",
                             foreignField: "_id",
                             as: "user_info"
                        }}
                        ,{$lookup:{
                             from: "department",
                             localField: "user_info.department",
                             foreignField: "_id",
                             as: "company_info"
                        }}
                        ,{$lookup:{
                             from: "department",
                             localField: "company_info.parentId",
                             foreignField: "_id",
                             as: "company"
                        }}
                        ,{$project:{'_id':1,'company.name':1,'company_info.name':1, "user_info.showImg":1, 'device_info.throughType':1,'device_info.name':1}}
                    ]).exec(function(err,result){                        
                        v_data['user_info']={
                            "sign_time": new Date(time_user[0]['updateTime']).toLocaleDateString(),
                            "direction": result[0]['device_info'][0]['throughType'] == 'in' ? '进入': '外出' ,
                            "name": time_user[0]['personName'],
                            "work_type": result[0]['company_info'][0]['name'],
                            "device_name": result[0]['device_info'][0]['name'],
                            "sign_avatar": 'http://192.168.1.144/'+time_user[0]['captureImg'],
                            "avatar": 'http://192.168.1.144/'+result[0]['user_info'][0]['showImg'],
                            "unit": result[0]['company'][0]['name']
                        }
                        console.log('查询数据库运行', ((new Date().getTime())-tc)/1000) // 查询数据库运行0.364
                        cb2()
                    })
                }],cb)
            }], function(err, result){
                // console.log('transit_trend', v_data) 
                run_t2=new Date().getTime()
                console.log('runtime', run_t2-run_t1) //1650
                e={
                    "msg": "成功",
                    "code": 200,
                    "data": v_data
                    ,"status": 'success'
                };
                res.send(e)
        })
    });

    api.get('/test', function(req, res, next){
        // 部门, 现场人数
        // 人员总数，进数，出数
        // 每个时间段的进数 ，出数，
        // 人员信息， 姓名，岗位，通道，方向，时间，比对照片
        var record = mongoose.model('record', recordSchema);
        record.find({}, function(err, use){
            console.log('err', err)
            console.log('use', use)
        })
        res.send('ok')
    })

    return api;
};