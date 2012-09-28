<!-- URL：list/find -->
<p align="left"><a href="../list">back</a></p>
<form method="post">
    <table>
        <tr><td width="100">ASIN:</td><td><input type="text" name="ASIN"></td></tr>
    </table>
    <input type="submit"value="find">
</form>
<?php
    require_once("SoapClient.php");
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
?> 
