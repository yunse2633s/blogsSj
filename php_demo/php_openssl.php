<?php
# openssl
$data=array(1,2,3);   //data可任意数据格式



//签名函数,rsaPrivateKeyFilePath私钥路径

function data_sign($data,$rsaPrivateKeyFilePath) {

	//读取私钥文件
	$priKey = file_get_contents($rsaPrivateKeyFilePath);

	///转换为openssl格式密钥
	$res = openssl_get_privatekey($priKey);
	echo 'a'.$priKey;

	// foreach (file_get_contents as $key => $value) {
	// 	# code...
	// 	echo $key .'=>'. $value;
	// }
	
	//签名需要把数组转换成字符串

	// $data=getSignContent($data);

	//签名
	// openssl_sign($data, $sign, $res);

	//释放资源
	// openssl_free_key($res);

	//转码
	// $sign = base64_encode($sign);

	// return $sign;
}

data_sign($data, "G:/work/blogsSj/php_demo/rsa_private_key.pem");

echo '<h3> if</h3>';

$t=date('H');

if($t<'20'){
	echo 'Time is '.$t;
}else{
	echo 'Time ';
}
echo '<br/>';
// printf(Array(1,2,3));
// printf([1,2,3]);
// echo ['1', '2', '3'];
// $xarr = Array('1', '3');
// $xarr = array('1', '3');
// printf $xarr;
// printf($xarr);
// $cars=array("Volvo","BMW","Toyota");
// echo $cars;
$cars=array('v','b');
echo '<br/>'.count($cars);
echo '<br/><b>var_dump:</b>';
var_dump($cars);
echo '<br/><b>print_r:</b>';
print_r($cars);
// var_dump([1,2,,3]);
echo '<br/><b>var_dump2:</b>';
echo '<pre>';
print_r([1,2,3]);
echo '</pre>';
print $t;