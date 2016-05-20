<?php
echo '<h2>函数</h2>';
echo '<h6>自定义函数</h6>';
function myselfun($x,$y){
	echo $x.'+'.$y.'='.($x+$y);
}
function myselfun2($x,$y){
	return $x.'+'.$y.'='.$x*$y;
}
myselfun(2,3);
echo '<br/>myselfun2返回值'.myselfun2(2,3);
// 演示数组函数的用法
echo '<h6>数组类函数</h6>';
$num=[10,1,2,3,5];
print_r($num);
echo '<br/>对数组进行(sort)升序排序'.sort($num).'<br/>';print_r($num);
echo '<br/>对数组进行(rsort)降序排序'.rsort($num).'<br/>';print_r($num);
$school=Array();
$school['hb']='河北';
$school['sh']='上海';
$school['yn']='云南';
echo '<br/>';
var_dump($school);
echo '<br/>对关联数组的值<code>(asort)</code>升序排序'.asort($school).'<br/>';print_r($school);
echo '<br/>对关联数组的值<code>(arsort)</code>降序排序'.arsort($school).'<br/>';print_r($school);
echo '<br/>对关联数组的键<code>(ksort)</code>升序排序'.ksort($school).'<br/>';print_r($school);
echo '<br/>对关联数组的键<code>(krsort)</code>降序排序'.krsort($school).'<br/>';print_r($school);
