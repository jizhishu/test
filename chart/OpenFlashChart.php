<?php
/**
 * 每日点击数图表

 * 工作中的一个案例，记录一下
 */
function addata_click_monitor(){
  $out = '';
  date_default_timezone_set('PRC');
  $curr_month = date('Y_m', time());
  $header = array(
      array('data' => '日期'),
      array('data' => '点击数')
  );
  $rows = array();

  $labels = array(); //图表x轴项目
  $values = array(); //图表项目数值
  $max = 0;



  $table = 'adclick_' . $curr_month;
  //$table = 'adclick_2011_08';
  $sql = "SELECT FROM_UNIXTIME( visit_gm_time, '%s' ) AS d, COUNT(*) as c FROM " . $table . " GROUP BY d "; //统计当月每天的点击数
  $res = db_query($sql, '%Y-%m-%d');
  while($item = db_fetch_object($res)){
    $rows[] = array(
      $item->d, // 日期
      $item->c  // 点击数
    );
    $max = $max > $item->c ? $max : $item->c; // 图表Y轴最大值
    array_push($labels, date('j', strtotime($item->d))); //图表x轴项目文本
    array_push($values, intval($item->c)); //图表X轴项目数值
  }

  //------------图表开始-----------
  $module_path = drupal_get_path('module', 'addata');

  $json_data = array();

  $json_data['title']['text']     = $curr_month . ' 广告点击数'; // 图表标题
  $json_data['title']['style']    = "{font-size: 18px; color:#0000ff; font-family: Verdana; text-align: center;}";

  $json_data['y_legend']['text']  = '';
  $json_data['y_legend']['style'] = "{color: #736AFF; font-size: 2px; font-family: simsun;}";
  $json_data['num_decimals']      = 0; // Y轴0位小数


  $json_data['elements'][0]['type']      = 'line';
  $json_data['elements'][0]['animate']   = true;
  $json_data['elements'][0]['alpha']     = 0.5;
  $json_data['elements'][0]['colour']    = '#9933CC';
  $json_data['elements'][0]['text']      = '点击数';
  $json_data['elements'][0]['font-size'] = 10;
  $json_data['elements'][0]['values']    = $values;

  $json_data['x_axis']['stroke']       = 1;
  $json_data['x_axis']['tick_height']  = 10;
  $json_data['x_axis']['colour']       = '#d000d0';
  $json_data['x_axis']['grid_colour']  = '#00ff00';
  $json_data['x_axis']['labels']['labels']       = $labels;
  //$json_data['x_axis']['labels']['rotate']       = 'vertical'; //x轴文字竖排

  $json_data['y_axis']['stroke']       = 1;
  $json_data['y_axis']['tick_length']  = 10;
  $json_data['y_axis']['colour']       = '#d000d0';
  $json_data['y_axis']['grid_colour']  = '#00ff00';
  $json_data['y_axis']['offset']       = 0;
  $json_data['y_axis']['max']          = intval($max); //Y轴最大值
  $json_data['y_axis']['steps']        = intval($max / 1000); //Y轴步长



  $json_data_content = json_encode($json_data);
  $f = fopen($module_path . '/Classes/openFlashChat/data/' . $curr_month . '.json', 'w+');
  fwrite($f, $json_data_content);
  fclose($f);


  drupal_add_js($module_path . '/Classes/openFlashChat/swfobject.js');
  drupal_add_js(
    'swfobject.embedSWF("' . $module_path . '/Classes/openFlashChat/open-flash-chart.swf", "my_chart", "100%", "300", "9.0.0","expressInstall.swf",{"data-file":"' . $module_path . '/Classes/openFlashChat/data/' . $curr_month . '.json"});', 'inline'
  );

  $out .= '<div id="my_chart" style="height:300px; color: #C10C02; border:1px solid #CCC">图表区</div>';

  //-----------图表结束--------

  return $out . theme('table', $header, $rows);
}
?>
