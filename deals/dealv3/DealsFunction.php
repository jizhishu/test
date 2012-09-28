<!--action result -->
<?php
function dealslist()
{
?>
<form method="post">
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
    $row=$soap->findAll();
     $n=count($row);//total items
     $n0=0;$n1=10;
     //show list
     //show pages
     if(isset($_GET['page']))
     {
          $n0=$_GET['page']*10;
          if($n0+10>$n)$n1=$n;
          else $n1=$n0+10;
      }
     else
     {
          if($n0+10>$n)$n1=$n;
          else $n1=$n0+10;
      }
       for($i=$n0;$i<$n1;$i++){
?>
      <tr bgcolor="#bbff">
          
          <td width="10"><input type="checkbox" name="chk[]" id="chk[]"value="<?php echo $row["$i"]["_id"];?>"></td>
          <td width="100"><?php echo $row["$i"]["_id"];?></td>
          <td width="100"><?php echo $row["$i"]["name"];?></td>
          <td width="100"><?php echo $row["$i"]["price"];?></td>
          <td width="100"><?php echo date('Y-m-d h:i:s a',strtotime($row["$i"]["expiration_time"]));?></td>
          <td width="100"><?php echo $row["$i"]["content"];?></td>
      </tr>
<?php
     }
?>
    </table>
    <p align="center">
<?php
    $n2=$n/10;
    //page
    for($i=0;$i<$n2;$i++)
    {
?>
    <td width="10">[<a href="?page=<?php echo $i;?>"><?php echo $i+1;?></a>]</td>
<?php
        }
?>
    </p>
    <p align="center"><?php  echo "Total  items:  ".$n; ?></p>
    <p align="left">
        <input type="radio" name="rad"  value="delete">delete
        <input type="radio" name="rad"  value="insert">insert
        <input type="radio" name="rad"  value="find">find
    </p>
    <p align="left">
        <input type="submit"  value="submit"> 
        <input type="reset"  value="reset">
    </p>
</form>
<?php
}
?>

<?php
function insert()
{
?>
<form method="post">
    <table>
        <tr><td width="100">ASIN:</td><td><input type="text" name="ASIN"></td></tr>
        <tr><td width="100">name:</td><td><input type="text" name="name"></td></tr>
        <tr><td width="100">price:</td><td><input type="text" name="price"></td></tr>
        <tr><td width="100">expiration_time:</td><td><input type="text" name="expiration_time"></td></tr>
        <tr><td width="100">content:</td><td><input type="text" name="content"></td></tr>
    </table>
        <input type="submit" value="insert">
</form>
<?php
    if(isset($_POST['ASIN']))
    {
        $ASIN=$_POST['ASIN'];
        $insert=0;
        $timey=date('Y',strtotime($_POST['expiration_time']));
        if($timey<2012||$timey>2100)drupal_set_message('illegal time!');
        else
        {
            $ASIN=$_POST['ASIN'];$name=$_POST['name'];$price=$_POST['price'];
            $expiration_time=$_POST['expiration_time'];$content=$_POST['content'];
            $deal=array(
                    "ASIN"=>"$ASIN",
                    "name"=>"$name",
                    "price"=>"$price",
                    "expiration_time"=>"$expiration_time",
                    "content"=>"$content"
              );
            $result=$soap->insert($deal);
            if($result!=false) header("Location:DealsMain");
            else drupal_set_message('Insert failed');
        }
    }
    else drupal_set_message('Please,input data!');
}
?> 

<?php 
function delete()
{
    //var_dump($_POST);
    $row=0;
    if(isset($_POST['chk']))
    {
        $chk=$_POST['chk'];
        $n=count($chk);
        for($i=0;$i<$n;$i++)
        {
           $result=$soap->deleteByAsin($chk[$i]);
           if($result==true){}
           else drupal_set_message('delete failed!');
        }
        if($result)header("Location:DealsMain");
    }
    else  drupal_set_message('Nothing deleted!');
}
?>

<?php
function find()
{
?>
<form method="post">
    <table>
        <tr><td width="100">ASIN:</td><td><input type="text" name="ASIN"></td></tr>
    </table>
    <input type="submit"value="find">
</form>
<?php
    if(isset($_POST['ASIN']))
    {
        $ASIN=$_POST['ASIN'];
        $result=$soap->findByAsin("$ASIN");
        if($result!=false)
        {
 ?> 
<form>find result:
    <table>
        <tr>
            <th width="100">ASIN</th>
            <th width="100">name</th>
            <th width="100">price</th>
            <th width="100">expiration_time</th>
            <th width="100">content</th>
        </tr>
        <tr>
            <td width="100"><?php echo $result["_id"];?></td>
            <td width="100"><?php echo $result["name"];?></td>
            <td width="100"><?php echo $result["price"];?></td>
            <td width="100"><?php echo $result["expiration_time"];?></td>
            <td width="100"><?php echo $result["content"];?></td>
        </tr>
    </table>
</form>
<?php
        }
    else drupal_set_message('No find！');
    }
    else drupal_set_message('ASIN is NULL！');
}
?> 
