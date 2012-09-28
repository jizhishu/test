<?php
    $soap_server="http://192.168.1.110/webservice/SoapMongo.php";
    //echo file_get_contents($soap_server);
    $uri="deal";
    $password="1234567";
    $soap=NULL;
    try{
        $soap=new SoapClient(NULL,array(
                                        "location"=>$soap_server,
                                        "uri"=>$uri,
                                        "style"=>SOAP_RPC,
                                        "use"=>SOAP_ENCODED,
                                        )
                             );
        $header=new SoapHeader($uri,"auth",$password,false,SOAP_ACTOR_NEXT);
        $soap->__setSoapHeaders(array($header));
    }catch(Exception $e){
        echo "Exception:".$e->getMessage();
    }
?>