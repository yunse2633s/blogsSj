<?php
//全局变量
//$GLOBALS,$_SERVER,$_REQUEST,$_POST,$_GET,$_FILES,$_ENV,$_COOKIE,$_SESSION
echo '<h4>php全局变量</h4>';
echo '<h6>$GLOBALS</h6>';
$x=75;
$y=25;
function addition(){
	$GLOBALS['z']=$GLOBALS['x']+$GLOBALS['y'];
}
addition();
echo 'addition函数内计算全局变量z的值'.$z;
echo '<h6>$_SERVER</h6>';
foreach($_SERVER as $key=>$value){
	echo $key.'、';
}
echo '<hr/>';
echo '<table>';
foreach($_SERVER as $key=>$value){
	echo '<tr>';
	echo '<td>'.$key.'</td><td>'.$_SERVER[$key].'</td>';
	echo '</tr>';
}
echo '</table>';
echo '<hr/>';
echo '<h6>$_REQUEST</h6>';
echo '$_REQUEST["fname"]:'.$_REQUEST['fname'];
echo <<<requestForm
<html>
	<head>
		<meta charset="utf-8" />
		<title>request</title>
	</head>
	<body>
		<form method="post" action="#">
		name:<input type="text" name="fname" />
		<input type="submit"/>
		</form>
	</body>
</html>
requestForm;

echo '<h6>$_POST</h6>';
$post_form=<<<postForm
<html>
	<head>
		<meta charset="utf-8" />
	</head>
	<body>
		<form method="post" action="#" >
			name:<input type="text" name="fname" />
			<input type="submit" />
		</form>
	</body>
</html>
postForm;
echo $post_form;
echo '$_POST["fname"]:'.$_POST['fname'];
echo '<h6>$_GET</h6>';
$get_form=<<<getForm
<html>
	<head>
		<meta charset="utf-8" />
	</head>
	<body>
		<form method="get" action="#" >
			name:<input type="text" name="fname" />
			<input type="submit" />

		</form>
	</body>
</html>
getForm;
echo $get_form;
echo '$_GET["fname"]:'.$_GET['fname'];

echo '<h6>$_FILES</h6>';
$file_form=<<<fileForm
<html>
	<head>
		<meta charset="utf-8" />
	</head>
	<body>
		<form method="post" action="#" enctype="multipart/form-data">
			name:<input type="file" name="fname" />
			<input type="submit" />
		</form>
	</body>
</html>
fileForm;
echo $file_form;
echo '$_FILES["fname"]:';var_dump($_FILES['fname']);

echo '<h6>$_ENV</h6>';
echo '<h6>$_COOKIE</h6>';
echo '<h6>$_SESSION</h6>';

