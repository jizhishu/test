<?php
$mongo = new Mongo("192.168.1.110:27017");
$query1=array("name"=>'new product');
$query2=array("name"=>'data acquisition');
$query3=array("name"=>'Analytic');
$cursor1=$mongo->amazon->system->find($query1);
$cursor2=$mongo->amazon->system->find($query2);
$cursor3=$mongo->amazon->system->find($query3);
?>
<?php
require_once 'XML/Serializer.php';
$options = array(
		'indent' => '',
		'addDecl' => false,
		'rootName' => "xml",//$fc->getAction(),
		XML_SERIALIZER_OPTION_RETURN_RESULT => true
	);
$serializer = new XML_Serializer($options);
$response=array('response'=>'66669');
header('Content-type:application/xml');
echo $serializer->serialize($response);

?>
