//http://www.tuicool.com/articles/UnuURf
Router.map(function () {
  this.route('serverFile', {
    where: 'server'
    ,path: '/files'
    ,onBeforeAction:function(){
      console.log("onBeforeAction")
      
    }
    ,action: function () {
      console.log("------ files------"+"\n"+this.request);
       app = new Array();
       for(var i in this.request){
               app.push(i);
               // console.log(i)
       }

      this.response.writeHead(200, {'Content-Type': 'text/html'});
      // var js = "<script> console.log("+this.request+")</script>"
      this.response.end("js");
      // --------------------
  }
  // ,onAfterAction:function(){
  //   console.log("after")
  // }



  });
});