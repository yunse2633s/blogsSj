// 参照 https://www.cnblogs.com/imwtr/p/4398652.html，获取2018安博会厂商列表
// 
var http = require('http');
var cheerio = require('cheerio');

// 安博会厂商列表
var url = 'http://www.securitychina.com.cn';

//安博会字符集为 gb2312，需转换
var iconv = require('iconv-lite');



http.get(url,function(res){  //通过get方法获取对应地址中的页面信息
	 console.log('1')
    var chunks = [];
    var size = 0;
    res.on('data',function(chunk){   //监听事件 传输
        chunks.push(chunk);
        size += chunk.length;
    });
    res.on('end',function(){  //数据传输完
        var data = Buffer.concat(chunks,size);  
        var html = iconv.decode(data,'gb2312'); 
        var $ = cheerio.load(html, {decodeEntities: false}); //cheerio模块开始处理 DOM处理
        var jobs = [];
        // var jobs_list = $(".hot_pos li"); //暂时没用 sj
        // var jobs_list = $(".body_1_left_mid_1_right li");

        // console.log( $(".body_1_left_mid_1_right").html() );
        $(".body_1_left_mid_1_right li").each(function(){   //对页面岗位栏信息进行处理  每个岗位对应一个 li  ,各标识符到页面进行分析得出
            // console.log('dd')
            // var job = {};
            // job.company = $(this).find(".hot_pos_r div").eq(1).find("a").html(); //公司名
            // job.period = $(this).find(".hot_pos_r span").eq(1).html(); //阶段
            // job.scale = $(this).find(".hot_pos_r span").eq(2).html(); //规模

            // job.name = $(this).find(".hot_pos_l a").attr("title"); //岗位名
            // job.src = $(this).find(".hot_pos_l a").attr("href"); //岗位链接
            // job.city = $(this).find(".hot_pos_l .c9").html(); //岗位所在城市
            // job.salary = $(this).find(".hot_pos_l span").eq(1).html(); //薪资
            // job.exp = $(this).find(".hot_pos_l span").eq(2).html(); //岗位所需经验
            // job.time = $(this).find(".hot_pos_l span").eq(5).html(); //发布时间
            var job = {};
            // console.log($(this).find("a").html());  //控制台输出岗位名
            job.url = $(this).find('a').attr('href');
            job.url = url +job.url;
            if($(this).find("font").length>0){
                job.name=$(this).find('a font').html();

            }else{
                job.name=$(this).find('a').html();
            }
            jobs.push(job);  
        
        });
        console.log( JSON.stringify(jobs) )
        // Res.json({  //返回json格式数据给浏览器端
        //     jobs:jobs
        // });
    });
});


// const $ = cheerio.load('<div class="body_1_left_mid_1_right"> <ul><li><span>10-19</span><a href="/2018blh/article/article_8300.html" target="_blank"><font color="red">2018安博会-活动日程表</font></a></li><li><span>09-30</span><a href="/2018blh/article/article_8296.html" target="_blank"><font color="red">参展商自带入馆的展具、家具、花卉和绿植申报延期通知</font></a></li><li><span>09-27</span><a href="/2018blh/article/article_8295.html" target="_blank">紧急通知：展商自带入馆的家具和绿植于9月30日前申报</a></li><li><span>09-26</span><a href="/2018blh/article/article_8294.html" target="_blank">“观展通”正式上线，加大展前和展中推广力度</a></li><li><span>09-20</span><a href="/2018blh/article/article_8293.html" target="_blank">现场报到、参展证件申请、展品运输等常见问题答疑</a></li><li><span>09-19</span><a href="/2018blh/article/article_8292.html" target="_blank">2018安博会《展商须知》发布</a></li><li><span>09-13</span><a href="/2018blh/article/article_8291.html" target="_blank">重要客户观展证件注册开启，可通过“客户邀请”完成</a></li><li><span>09-12</span><a href="/2018blh/article/article_8290.html" target="_blank">观众注册窗口开放了，观展报名、客户邀请方式及流程</a></li></ul> </div>')
 
// // $('h2.title').text('Hello there!')
// $('h2').addClass('welcome')
 
// console.log($('.body_1_left_mid_1_right>ul>li').eq(0).html())
