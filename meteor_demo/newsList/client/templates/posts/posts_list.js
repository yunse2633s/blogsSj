// var postsData=[
// 	{
// 		title:'Introducing Telescope',
// 		url:'http://sachagref.com'
// 	},
// 	{
// 		title:'Meteor'
// 		,url:'http://meteor.com'
// 	}
// 	,{
// 		title:'The Meteor Book'
// 		,url:'http://themeteorbook.com'
// 	}
// ];

Template.postsList.helpers({
	// posts:postsData
	// posts:function(){;
	// 	return Posts.find({},{sort:{submitted:-1}});
	// }
});
Template.postsList.rendered=function(){
	this.find('.wrapper')._uihooks={
		insertElement:function(node,next){
			$(node)
				.hide()
				.insertBefore(next)
				.fadeIn();
		}
		,moveElement:function(node,next){
			// console.log(node,next);
			var $node = $(node),$next = $(next);
			var oldTop = $node.offset().top; //取得元素相对文档的当前位置，返回top和left
			var height = $node.outerHeight(true); //取得"outer"元素的高度(含padding\margin)
			// 找出next与node之间所有的元素
			var $inBetween = $next.nextUntil(node); //取得所有目标元素之后到匹配node的元素
			if($inBetween.length===0){
				$inBetween = $node.nextUntil(next);
			}
			// 把node放在预定位置
			$node.insertBefore(next); //在匹配next的元素之前插入另外一个元素
			// 测量新top偏移坐标
			var newTop=$node.offset().top;
			// 将node移动至原始所在位置
			$node.removeClass('animate'); //如果元素有'animate'，则删除它
			$node.css('top',oldTop-newTop); //设置css的属性'top'为oldTop-newTop
			$inBetween.removeClass('animate');
			$inBetween.css('top',oldTop < newTop ? height : -1*height)
			// 强制重绘
			$node.offset();
			// 动画,重置所有元素的top坐标为0
			$node.addClass('animate').css('top',0); //为元素添加class类
			$inBetween.addClass('animate').css('top',0);

		}
		,removeElement:function(node,next){
			$(node).fadeOut(function(){
				$(this).remove();
			})
		}
	}
}