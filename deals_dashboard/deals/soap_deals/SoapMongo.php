<?php
    function getShellText($f,$s=NULL)
    {
	$para="";
	if($s!=NULL)
	{
        	$json=json_encode($s);
        	$para="\"".str_replace("\"","\\\"",$json)."\"";
        }
        return "python mongo/mongo_API.py ".$f." ".$para;
    }
    function getResult($s)
    {
        $json=strstr($s,"{");
        
        return json_decode($json,true);
    }
    
    
    class deal
    {
        public function auth($password)
        {
            if($password!="1234567")
                throw new SoapFault('Server',"Access denied!");
        }
        function test($text)
        {
            $return_text=system("python mongo/test_py.py",$result);
            if($result==0)
            return $return_text.":".$text;
            else return "failed".":".$text;
        }
        
        
        function insert($deal)
        {
            /*
             Sample input:
             $deal=array(
                         "ASIN"=>"12345",
                         "name"=>"test",
                         "price"=>"100",
                         "expiration_time"=>"2011-07-20 16:04:10",
                         "content"=>"test content"
             );
            */ 
            
            $result=system(getShellText("dealsInsert",$deal),$flag);
            if($flag==0)
            {
                $s=getResult($result);
                if(isset($s["flag"]))
                    if($s["flag"]=="Success")return true;
                return false;
            }
            else
                return false;
        }

	function findAll()
        {
            $result=system(getShellText("dealsSearchAll"),$flag);
            if($flag==0)
            {
                $record=getResult($result);
                if(isset($record["results"]))
                    return $record["results"];
                else
                    return false;
            }
            else
                return false;
        }
        
        function findByAsin($asin)
        {
            $result=system(getShellText("dealsSearchByASIN",array("asin"=>$asin)),$flag);
            if($flag==0)
            {
                $record=getResult($result);
                if(isset($record["results"][0]))
                    return $record["results"][0];
                else
                    return false;
            }
            else
                return false;
        }
        function deleteByAsin($asin)
        {
            $result=system(getShellText("dealsDeleteByASIN",array("asin"=>$asin)),$flag);
            if($flag==0)
            {
                $s=getResult($result);
                if(isset($s["flag"]))
                    if($s["flag"]=="Success")return true;
                return false;
            }
            else
                return false;
        }
    }
    $server_deal=new SoapServer(NULL,array("uri"=>"deal"));
    $server_deal->setClass("deal");
    $server_deal->handle();
?>
