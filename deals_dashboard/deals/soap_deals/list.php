<!-- URL：list -->
<?php
    require_once("SoapClient.php");
    $row=$soap->findAll();
    //echo "FindAll:<br>" ;
    //var_dump($row);
    if($row!=false){
?>
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
         $n=count($row);//total items
         $n0=0;$n1=20;
         //show list
         //show pages
         if(isset($_GET['page']))
         {
              $n0=$_GET['page']*20;
              if($n0+10>$n)$n1=$n;
              else $n1=$n0+20;
          }
         else
        {
              if($n0+20>$n)$n1=$n;
              else $n1=$n0+20;
          }
           for($i=$n0;$i<$n1;$i++){
           //echo "<br>row _id:<br>";
           //var_dump($row["$i"]["_id"]);
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
         $n2=$n/20;
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
        <input type="button" value='insert' onclick="window.location.href='list/insert'">
        <input type="button" value='find' onclick="window.location.href='list/find'">
        <input type="submit"  value="delete"> 
        <input type="reset"  value="reset">
    </p>
</form>
<?php
    }
    else echo "Error!";
?>
