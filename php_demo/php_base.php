<?php
// 语法，变量，数据类型，常量，字符串，运算符，数组，
$x=5;
$y=6;
$_z3=$x+$y;
echo '<h5>变量的作用域</h5>';
echo '变量$_z3的结果'.$_z3."\n";

// 变量的作用域:local,global,static,parameter

// global $XYZ="红旗不倒 彩旗飘飘";
function x(){
	global $x;
	echo "<br>x()中输出全局变量".$x;
	// 全局变量存储在一个名为 $GLOBALS[index] 的数组中。
	// index 保存变量的名称
	echo '<br>$GLOBALS["y"]='.$GLOBALS['y'];
}
x();

// static作用域
function myTest(){
	static $x=0;
	$y='你猜';
	echo '<br/>'.$x.$y;
	$x++;
	$y=$y.$x;
}
echo '<br/>static作用域下的变量值不会随函数的结束而被被删除<br/>';
myTest();
myTest();
myTest();

// 7种数据类型：String（字符串）, Integer（整型）, Float（浮点型）, Boolean（布尔型）, Array（数组）, Object（对象）, NULL（空值）
// 整型
echo("<h5>7种数据类型</h5>");
$x=5;
var_dump($x);
$x=-5;
var_dump($x);
$x=0x8;
var_dump($x);
$x=047;
var_dump($x);

echo("<br/>浮点型");
$x=10.2;
var_dump($x);
$x=2.4e3;
var_dump($x);
$x=8E-5;
var_dump($x);

echo '<br/>布尔型';
$x=false;
var_dump($x);
$x=true;
var_dump($x);

echo '<br/>数组型';
$x=array('val',['a'],true,3);
var_dump($x);

echo '<br/>对象';
class Car{
	var $color;
	function Car($color='green'){
		$this->color=$color;
	}
	function what_color(){
		return $this->color;
	}
}
var_dump(Car);

echo '<br/>null值';
var_dump($xx);
//  define() 函数设置常量
/**
* constant_name：必选参数，常量名称，即标志符
* value：必选参数，常量的值
* case_insensitive：可选参数，指定是否大小写敏感，设定为 true 表示不敏感
*/
echo '<br/>define()设置常量';
define('HWORLD',"欢迎来到三体世界",true);
define('DESC','请介绍你的来意');
echo '<br/>'.hworld.'<br/>'.DESC;

// 算术运算符 + - * / % . intdiv()
echo '<h5>算术运算符</h5>';
echo '<br/> php7.0 intdiv()整除运算符';
echo '<br/>2+2='.(2+2);
echo '<br/>2-2='.(2-2);
echo '<br/>2*2='.(2*2);
echo '<br/>2/2='.(2/2);
echo '<br/>2%2='.(2%2);
echo '<br/>2.2='.(2.2);

// var_dump(intdiv(10,3));//
// 赋值运算符 = += -= *= /= %= .=
echo '<h5>赋值运算符</h5>';
echo '<br/>$x='.($x=2);
echo '<br/>$x +=2等于'.($x += 2);
echo '<br/>$x -=2等于'.($x -= 2);
echo '<br/>$x *=2等于'.($x *= 2);
echo '<br/>$x /=2等于'.($x /= 2);
echo '<br/>$x %=2等于'.($x %= 2);
// 递增递减运算符 ++ --
$x=3;
echo '<h5>递增递减运算符</h5>';
echo '<br/>$x的值为:'.$x;
echo '<br/>++$x = '.++$x;
echo '<br/>$x的值为:'.$x;
echo '<br/>$x++ = '.$x++;
echo '<br/>$x的值为:'.$x;
echo '<br/>--$x = '.--$x;
echo '<br/>$x的值为:'.$x;
echo '<br/>$x-- = '.$x--;
echo '<br/>$x的值为:'.$x;
// 比较运算符 == === != <> !== > < >= <=
$y = '3';
echo '<h5>比较运算符</h5>';
var_dump($y);
echo '<h5>当$x=3,$y="3"时:</h5>';
echo '<br/>$x==$y是真假:';var_dump($x==$y);
echo '<br/>$x===$y是真假:';var_dump($x===$y);
echo '<br/>$x!=$y是真假:';var_dump($x!=$y);
echo '<br/>$x<>$y是真假:';var_dump($x<>$y);
echo '<br/>$x>$y是真假:';var_dump($x>$y);
echo '<br/>$x>=$y是真假:';var_dump($x>=$y);
echo '<br/>$x<=$y是真假:';var_dump($x<=$y);

// 逻辑运算符
echo("<h5>逻辑运算符</h5>");
$a=[1,0];
$b=[1,0];
for($i=0;$i<=1;$i++){
	for($j=0;$j<=1;$j++){
		echo "<br/>$a[$i] and $b[$j] ";var_dump($a[$i] and $b[$j] );
	}
}
echo '<hr/>';
for($i=0;$i<=1;$i++){
	for($j=0;$j<=1;$j++){
		echo "<br/>$a[$i] or $b[$j] ";var_dump($a[$i] or $b[$j] );
	}
}
echo '<hr/>';
for($i=0;$i<=1;$i++){
	for($j=0;$j<=1;$j++){
		echo "<br/>$a[$i] xor $b[$j] ";var_dump($a[$i] xor $b[$j] );
	}
}
echo '<hr/>';
for($i=0;$i<=1;$i++){
	for($j=0;$j<=1;$j++){
		echo "<br/>$a[$i] && $b[$j] ";var_dump($a[$i] && $b[$j] );
	}
}
echo '<hr/>';
for($i=0;$i<=1;$i++){
	for($j=0;$j<=1;$j++){
		echo "<br/>$a[$i] || $b[$j] ";var_dump($a[$i] || $b[$j] );
	}
}
echo '<hr/>';
for($i=0;$i<=1;$i++){
	for($j=0;$j<=1;$j++){
		echo "<br/>!$a[$i]";var_dump(!$a[$i]);
	}
}
echo '<hr/>';
echo '<h5>三元运算符</h5>';
$username=isset($_GET['user']) ? $_GET['user'] : '暂无' ;
echo '地址栏中user值为:'.$username;
// php5.3+版本的另外一种写法
$username=$_GET['user'] ?: '暂无';
echo '<br/>php5.3写法中地址栏user值:'.$username;
// php7+ 增加 组合比较符 <=>  大于1，相等0，小于-1
