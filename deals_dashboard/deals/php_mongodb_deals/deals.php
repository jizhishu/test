<!-- URL：deals -->
<?php
try{
    $mongo = new Mongo("192.168.1.110:27017");
?>
<form action="deals/result"method="post">
    <table>
        <tr bgcolor="yellow">
            <th width="10"></th>
            <th width="100">ASIN</th>
            <th width="100">name</th>
            <th width="100">price</th>
            <th width="100">expiration_time</th>
            <th width="100">content</th>
        </tr>
<?php
    $deals=$mongo->amazon->deals;
    $row=$deals->find()->sort( array( '_id' => 1 ) );//find all data,return MongoCursor Object
    $n=$deals->count();//total items
    foreach($row as $o){
            $timey=date('Y',strtotime($o['expiration_time']));
            if($timey<2012) $time='illegal time:'.$o['expiration_time'];
            else $time=date('Y-m-d h:i:s a',strtotime($o['expiration_time']));
?>
      <tr bgcolor="#bbff">
          <td width="10"><input type="checkbox" name="chk[]" id="chk[] "value="<?php echo $o['_id'];?>"></td>
          <td width="100"><?php echo $o['_id'];?></td>
          <td width="100"><?php echo $o['name'];?></td>
          <td width="100"><?php echo $o['price'];?></td>
          <td width="100"><?php echo $time;?></td>
          <td width="100"><?php echo $o['content'];?></td>
      </tr>
<?php
     }
?>
    </table>
    <p align="center"><?php  echo "Total Items: ".$n; ?></p>
    <p align="left">
        <input type="radio" name="rad"  value="delete">delete
        <input type="radio" name="rad"  value="update">update
        <input type="radio" name="rad"  value="insert">insert
        <input type="radio" name="rad"  value="find">find
    </p>
    <p align="left">
        <input type="submit"  value="submit"> 
        <input type="reset"  value="reset">
    </p>
</form>
<?php
    $mongo->close();
}
catch(MongoConnectionException $e) {
//handle connection error
//die($e->getMessage());
echo "handle connection error!<br>serverip:192.168.1.110<br>port:27017";
}
?>
