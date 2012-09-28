<?php
include("http://localhost/22222/FusionChartsFree/Code/PHP/Includes/FusionCharts.php");
?>

<HTML>
   <HEAD>
      <TITLE>mytestchart</TITLE>
      <SCRIPT LANGUAGE="Javascript" SRC="http://localhost/22222/FusionChartsFree/JSClass/FusionCharts.js"></SCRIPT>
   </HEAD>
   <BODY>
   <CENTER/>
   <?php

   //Connect to the DB
   $mongo = new Mongo("192.168.1.110:27017");
   $query[]=array("name"=>'new product');
   $query[]=array("name"=>'data acquisition');
   $query[]=array("name"=>'Analytic');
   foreach($query as $q)
      $cursor[]=$mongo->amazon->system->find($q);
   for($i=0;$i<3;$i++)
      foreach($cursor[$i] as $c){
        $result[$i][]=array(
                      "name"=>$c['name'],
                      "value"=>$c['value'],
                      "updatetime"=>$c['updatetime'],
                   );
       }
   //$strXML will be used to store the entire XML document generated
   //Generate the graph element
   $strXML = "<graph caption='system' subCaption='value' decimalPrecision='0' showNames='1' showValues='1' xAxisName= 'date' yAxisName= 'value' yAxisMinValue='100' yAxisMaxValue='200' rotateNames='1' formatNumberScale='0'>";

   //Iterate through each factory
   $strXML .= "<categories>";
   foreach($result[1] as $ors) {
         $strXML .= "<category name='" . $ors['updatetime']."' />";
         //free the resultset
      }
       $strXML .= "</categories>";
   $color[0]='1D8BD1';$color[1]='F1683C';$color[2]='2AD62A';
   for($j=0;$j<3;$j++){
      if ($result[$j]) {
          $strXML .= "<dataset seriesName='".$result[$j][1]['name']."' color='".$color[$j]."' anchorBorderColor='".$color[$j]."' anchorBgColor='".$color[$j]."'>";
         foreach($result[$j] as $ors) {
          //Generate <set name='..' value='..'/>
         $strXML .= "<set value='" . $ors['value'] . "' />";
         //free the resultset
          }
      $strXML .= "</dataset>";
   }
   }
   //Finally, close <graph> element
   $strXML .= "</graph>";
   //echo renderChart("http://localhost/22222/FusionChartsFree/Charts/FCF_MSLine.swf", "", $strXML, "mychart", 650, 450);
   //echo renderChart("http://localhost/22222/FusionChartsFree/Charts/FCF_MSLine.swf", "http://localhost/22222/FusionChartsFree/Gallery/Data/MSLine.xml", "", "mychart", 650, 450);
header('Content-type:application/xml');
echo $strXML;
?>
</BODY>
</HTML>
