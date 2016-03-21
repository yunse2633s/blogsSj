Meteor.publish('Its',function(options){
	return Its.find();
});

// serverMessages = new ServerMessages();
// console.log(serverMessages);

// Meteor.startup(function () {
//     Notifications.defaultOptionsByType[Notifications.TYPES.ERROR] = _.defaults({
//         timeout: 10000
//     },
//     Notifications.defaultOptions);
// });