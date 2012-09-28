<form>
<font size=5>System Operation Performance</font> 
<script language="JavaScript" src="http://localhost/drupal/FusionChartsFree/JSClass/FusionCharts.js"></script>
<td valign="top" class="text" align="left"> 
   <div id="chartdiv" align="left"> FusionCharts. </div>
   <script type="text/javascript">
      var chart = new FusionCharts("http://localhost/drupal/FusionChartsFree/Charts/FCF_MSLine.swf", "ChartId", "600", "400");
      chart.setDataURL("http://localhost/drupal/data.php");		   
      chart.render("chartdiv");
   </script>
</td>
</form>
<form>
<font size=5>Error Handing</font> 
<MARQUEE scrollAmount=1 scrollDelay=70 direction=up height=140>
<ul>
<?php
   $day=date("Ymd",strtotime("-7 day"));
   $mongo = new Mongo("192.168.1.110:27017");
   $query=array("time"=>array('$gt'=>$day));
   $cursor=$mongo->amazon->error_log->find($query)->sort(array('updatetime'=>1));
   foreach($cursor as $c){
        $result[]=array(
                      "type"=>$c['type'],
                      "description"=>$c['description'],
                      "rank"=>$c['rank'],
                      "time"=>$c['time'],
                   );
       }
    $mongo->close();
    $n=$cursor->count();
    while($n--){
?>
<li><?php echo $result[$n]['type']." ".$result[$n]['rank']." ".date("Y-m-d h:m:s a",strtotime($result[$n]['time']))." ".$result[$n]['description'];?></li>
<?php
}
?>
</ul>
</MARQUEE> 
</form>
