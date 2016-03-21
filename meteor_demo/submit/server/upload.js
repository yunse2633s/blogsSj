form = new formidable.IncomingForm();   //创建上传表单
form.encoding = 'utf-8';		//设置编辑
AVATAR_UPLOAD_FOLDER = '/avatar/';
form.uploadDir = 'public' + AVATAR_UPLOAD_FOLDER;	 //设置上传目录
form.keepExtensions = true;	 //保留后缀
form.maxFieldsSize = 2 * 1024 * 1024;   //文件大小

   // console.log(form.parse)
// 如何获取当前路径呢?
 // var a = fs.renameSync("../../../../../public/2.txt","../../../../../public/img/3.txt");
 // console.log(a)

Meteor.methods({
  upfile:function(req,res){
    console.log(form.parse);
  form.parse(req, function(err, fields, files) {

      if (err) {
        res.locals.error = err;
        res.render('index', { title: TITLE });
        return;		
      }  
       
      var extName = '';  //后缀名
      switch (files.fulAvatar.type) {
        case 'image/pjpeg':
          extName = 'jpg';
          break;
        case 'image/jpeg':
          extName = 'jpg';
          break;		 
        case 'image/png':
          extName = 'png';
          break;
        case 'image/x-png':
          extName = 'png';
          break;		 
      }

      if(extName.length == 0){
          res.locals.error = '只支持png和jpg格式图片';
          res.render('index', { title: TITLE });
          return;				   
      }

      var avatarName = Math.random() + '.' + extName;
      var newPath = form.uploadDir + avatarName;

      console.log(newPath);
      fs.renameSync(files.fulAvatar.path, newPath);  //重命名
    })
  	}
});