Router.configure({
    layoutTemplate: 'layout',
    // // notFoundTemplate: 'notFound',
    // progressSpinner: true,
    // progressDelay: 200,
    // loadingTemplate: 'loading'
});


Router.route('/', {name: 'home'});                              //测试
Router.route('/itSubmit', {name: 'itSubmit'});                            //测试3
Router.route('/method',{name:'method'});
Router.route('/abc',{name:'abc'});
Router.route('/jqUpload',{name:'jqUpload'});
Router.route('/methods',{name:'methods'});
Router.route('/upfile',{
	name:'upfile'
	// ,
});
Router.route('/up2',{
	name:'up2',
	onAfterAction:function(){
		console.log("e")
	}
})