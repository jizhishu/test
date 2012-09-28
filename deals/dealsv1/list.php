<!-- URL：list -->
<p align="left"><a href="list/insert">insert</a>&nbsp &nbsp &nbsp<a href="list/find">find</a></p>
<form action="list/delete"method="post">
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
    require_once("SoapClient.php");
    $row=$soap->findAll();
     //echo "FindAll:" ;
     //var_dump($row);
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
      <tr>
          <td width="10"><input type="checkbox" name="chk[]" id="chk[]"value=<?php echo $row["$i"]["_id"];?>></td>
          <td width="100"><?php echo $row["$i"]["_id"];?></td>
          <td width="100"><?php echo $row["$i"]["name"];?></td>
          <td width="100"><?php echo $row["$i"]["price"];?></td>
          <td width="100"><?php echo $row["$i"]["expiration_time"];?></td>
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
    <td width="10"><a href="?page=<?php echo $i;?>"><?php echo $i+1;?></a></td>
<?php
        }
?>
    </p>
    <p align="center"><?php  echo "Total: ".$n." items"; ?></p>
    <p align="left">
        <input type="submit"  value="delete"> 
        <input type="reset"  value="reset">
    </p>
</form>
