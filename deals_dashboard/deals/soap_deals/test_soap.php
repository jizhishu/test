<?php
    require_once("SoapClient.php");
    $deal=array(
                "ASIN"=>"1234567",
                "name"=>"test",
                "price"=>"100",
                "expiration_time"=>"2011-07-20 16:04:10",
                "content"=>"test content"
                );
    //echo getShellText("asdgsd",$deal);
    echo "<br>====<br>";
    $result=$soap->test("Hello");
    echo $result;
    echo "<br>====<br>";
    $result2=$soap->insert($deal);
    if($result2!=false){echo "insert:";var_dump($deal);}
    else echo "insert failed";
    echo "<br>====<br>";
    $result0=$soap->findAll();
    if($result0!=false){echo "findAll:";var_dump($result0);}
    else echo "findAll failed";
    echo "<br>====<br>";
    $result3=$soap->findByAsin("1234567");
    if($result3!=false){echo "find:";var_dump($result3);}
    else echo "find failed";
    echo "<br>====<br>";
    $result4=$soap->deleteByAsin("1234567");
    if($result4==true){echo "delete:"."1234567";}
    else echo "delete failed";
    echo "<br>====<br>";
    $result0=$soap->findAll();
    if($result0!=false){echo "findAll:";var_dump($result0);}
    else echo "findAll failed";
?>