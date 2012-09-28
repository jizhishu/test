<!-- URL：deals -->
<?php
    require_once("SoapClient.php");
    require_once("DealsFunction.php");
    dealslist();
    if(isset($_POST['rad'])&&($_POST['rad']=='delete'))delete();
    if(isset($_POST['rad'])&&($_POST['rad']=='insert'))insert();
    if(isset($_POST['rad'])&&($_POST['rad']=='find'))find();
?>
