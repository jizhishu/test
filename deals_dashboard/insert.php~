<!-- URL：list/insert -->
<p align="left"><a href="../list">back</a></p>
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
    require_once("SoapClient.php");
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
            if($result!=false) header("Location:../list");
            else drupal_set_message('Insert failed');
        }
    }
    else drupal_set_message('Please,input data!');
?> 
