<?php
echo '<pre>';
//$mongo = new Mongo();//create a connection to localhost
$mongo = new Mongo("192.168.1.110:27017"); //create a connection to MongoDB serverip=192.168.1.110 port=27017

$databases = $mongo->listDBs(); //List all databases. type：Array

$aa=$mongo->amazon->deals;//select table. type：MongoCollection

//new MongoDate();//MongoDate Object

$deals=array(
                "_id"=>"1234567",
                "name"=>"test",
                "price"=>"100",
                "expiration_time"=>"2011-07-20 16:04:10",
                "content"=>"test content"
                );
/*
OR

//$deals=array();
$deals['_id']='1234';
$deals['name']='test';
$deals['price']='1234';
$deals['expiration_time']='2012-05-06 11:22:33';
$deals['content']='content 1234';
*/
$insert=$mongo->amazon->deals->insert($deals);//insert

$obj=$aa->findOne();//Get the first data

$count=$aa->count();//count data

$obj=$aa->find();//find all data,return MongoCursor Object
//print find result
foreach($obj as $a){
	echo "ASIN:".$a['_id']."<br>";
	echo "name:".$a['name']."<br>";
	echo "price:".$a['price']."<br>";
	echo "expiration_time:".$a['expiration_time']."<br>";
	echo "content:".$a['content']."<br>";
	var_dump($a);
	print_r($a);
}

$query=array("_id"=>'1234567');//query condition (查询条件)
//$query=array("_id"=>array('$gt'=>50));//$gt:'>';$lt:'<';$gte:'>=';$lte:'<='
//$query=array("_id"=>array('\$gt'=>50,'\$lte'=>30));//Multiple query conditions
$cursor=$aa->find($query);//find by query

foreach($cursor as $a){
	echo "ASIN:".$a['_id']."<br>";
	echo "name:".$a['name']."<br>";
	echo "price:".$a['price']."<br>";
	echo "expiration_time:".$a['expiration_time']."<br>";
	echo "content:".$a['content']."<br>";
	var_dump($a);
	print_r($a);
}

//print find result
/*while($curor->hasNext()){
	var_dump($curor->hasNext());
}
*/
/*
*others:
*update($a,$newa)
*remove($a,$query)
*insert($a,$query)
*findOne($query)
*ensureIndex($query)
*http://fangdongqing.blog.51cto.com/3293821/603372
*/

?>

