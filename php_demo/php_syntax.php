<?php
// 判断 循环 
echo '<h5>循环与判断</h5>';
$x=true;
echo '<h6>if循环</h6>';
if($x){
  echo '$x为真';
}
$x=70;
if($x<=60){
	$y='及格';
}else if($x>=70 && $x<80){
	$y='良';
}else{
	$y='异常';
}
echo '<br/>$x的成绩'.$x.'为'.$y;

echo '<h6>switch循环</h6>';
switch($x){
	case $x>0 && $x<60:
		$y = '不及格';
		break;
	case $x>=60 && $x <70;
		$y ='及格';
		break;
	case $x>=70 && $x<90;
		$y='合格';
		break;
	default:
		$y='非法';
}
echo '<br/>$x的成绩'.$x.'为'.$y;
echo '<h6>for循环</h6>';
echo '<table>';
for($x=1;$x<=9;$x++){
	echo '<tr>';
	for($j=1;$j<=$x;$j++){
		echo '<td >'.$x.'*'.$j.'='.$x*$j.'</td>';
	}
	echo '</tr>';
}
echo '</table>';
echo '<h6>foreach的用法</h6>';
foreach($_GET as $key=>$value ){
	echo $key.'=>'.$value.'<br/>';
}
echo '<h6>while</h6>';
$x=1;
while($x<=3){
	echo '<br/>while循环次数($x<=3):'.$x;
	$x++;
}
echo '<h6>do...while</h6>';
do{
	echo '<br/>do...while循环($x<=2)';
	$x--;
}while($x<=2);
