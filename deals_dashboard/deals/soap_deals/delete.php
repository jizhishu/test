<!-- URL：list/delete -->
<p align="left"><a href="../list">back</a></p> 
<?php 
    //var_dump($_POST);
    require_once("SoapClient.php");
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
       if($result)header("Location:../list");
    }
    else  drupal_set_message('Nothing deleted!');
?>
