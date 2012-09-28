<?php
class build_graph{
    var $graphwidth=300;
    var $graphheight=300;
    var $width_num=0;
    var $height_num=10;
    var $width_var=0;
    var $height_var=0;
    var $height_max=0;
    var $array_data=array();
    var $array_error=array();
    var $colorBg=array(255,255,255);
    var $colorGrey=array(192,192,192);
    var $colorBlue=array(0,0,255);
    var $colorRed=array(255,0,0);
    var $colorDarkBlue=array(0,0,255);
    var $colorLightBlue=array(200,200,255);
    var $array_color;
    var $image;
    function add_data($array_user_data)
    {
        if(!is_array( $array_user_data) or empty($array_user_data))
        {
            $this->array_error['add_data']="NO DATA!";
            return false;
            exit();
        }
        $i=count($this->array_data);
        $this->array_data[$i]=$array_user_data;
    }
    function set_img($img_width,$img_height)
    {
        $this->graphwidth=$img_width;
        $this->graphheight=$img_height;
    }
    function set_height_num($var_y)
    {
        $this->height_num=$var_y;
    }
    function get_RGB($color)
    {
        $R=($color>>16)&0xff;
        $G=($color>>8)&0xff;
        $B=($color)&0xff;
        return (array($R,$G,$B));
    }
    function set_color_bg($c1,$c2,$c3)
    {
        $this->colorBg=array($c1,$c2,$c3);
    }
    function set_color_Grey($c1,$c2,$c3)
    {
        $this->colorGrey=array($c1,$c2,$c3);
    }
    function set_color_Blue($c1,$c2,$c3)
    {
        $this->colorBlue=array($c1,$c2,$c3);
    }
    function set_color_Red($c1,$c2,$c3)
    {
        $this->colorRed=array($c1,$c2,$c3);
    }
    function set_color_DarkBlue($c1,$c2,$c3)
    {
        $this->colorDarkBlue=array($c1,$c2,$c3);
    }
    function set_color_LightBlue($c1,$c2,$c3)
    {
        $this->colorLightBlue=array($c1,$c2,$c3);
    }
    function get_width_num()
    {
        $this->width_num=count($this->array_data[0]);
    }
    function get_max_height()
    {
        $tmpvar=array();
        foreach($this->array_data as $tmp_value)
        {
            $tmpvar[]=max($tmp_value);
        }
        $this->height_max=max($tmpvar);
        return max($tmpvar);
    }
    function get_height_length()
    {
        $max_var=$this->get_max_height();
        $max_var=round($max_var/$this->height_num);
        $first_num=substr($max_var,0,1);
        if(substr($max_var,1,1))
        {
            if(substr($max_var,1,1)>=5)
                 $first_num+=1;
        }
        for($i=1;$i<strlen($max_var);$i++)
        {
            $first_num.="0";
        }
        return (int)$first_num;
    }
    function get_var_wh()
    {         
        $this->get_width_num();
        $this->height_var=$this->get_height_length();
        $this->width_var=round($this->graphwidth/$this->width_num);
    }
    function set_colors($str_colors)
    {
        $this->array_color=split(",",$str_colors);
    }
    function build_line($var_num)
    {
        if(!empty($var_num))
        {
            $array_tmp[0]=$this->array_data[$var_num-1];
            $this->array_data=$array_tmp;
        }
        for($j=0;$j<count($this->array_data);$j++)
        {
            list($R,$G,$B)=$this->get_RGB(hexdec($this->array_color[$j]));
            $colorBlue=imagecolorallocate($this->image,$R,$G,$B);
            $i=0;
            foreach($this->array_data[$j] as $keys=>$values)
             {
                $height_next_pix[]=round($this->array_data[$j][$keys]/$this->height_max*$this->graphheight);
             }
            foreach($this->array_data[$j] as $key=>$value)
             {
                $height_pix=round(($this->array_data[$j][$key]/$this->height_max)*$this->graphheight);
                if($i!=count($this->array_data[$j])-1)
                {
                imageline($this->image,$this->width_var*$i,$this->graphheight-$height_pix,$this->width_var*($i+1),$this->graphheight-$height_next_pix[$i+1],$colorBlue);
                }
                $i++;
             }
         }
        $colorRed=imagecolorallocate($this->image, $this->colorRed[0], $this->colorRed[1], $this->colorRed[2]);
        for($j=0;$j<count($this->array_data);$j++)
        {
            $i=0;
            foreach($this->array_data[$j] as $key=>$value)
              {
                $height_pix=round(($this->array_data[$j][$key]/$this->height_max)*$this->graphheight);
                imagearc($this->image,$this->width_var*$i,$this->graphheight-$height_pix,6,5,0,360,$colorRed);
                imagefilltoborder($this->image,$this->width_var*$i,$this->graphheight-$height_pix,$colorRed,$colorRed);
                $i++;
              }
        }
    }
    function build_rectangle($select_gra)
    {
        if(!empty($select_gra))
        {
            $select_gra-=1;
        }
        $colorDarkBlue=imagecolorallocate($this->image, $this->colorDarkBlue[0], $this->colorDarkBlue[1], $this->colorDarkBlue[2]);
        $colorLightBlue=imagecolorallocate($this->image, $this->colorLightBlue[0], $this->colorLightBlue[1], $this->colorLightBlue[2]);
        if(empty($select_gra))
            $select_gra=0;
        for($i=0; $i<$this->width_num; $i++)
        {
           $height_pix=round(($this->array_data[$select_gra][$i]/$this->height_max)*$this->graphheight);
           imagefilledrectangle($this->image,$this->width_var*$i,$this->graphheight-$height_pix,$this->width_var*($i+1),$this->graphheight, $colorDarkBlue);
           imagefilledrectangle($this->image,($i*$this->width_var)+1,($this->graphheight-$height_pix)+1,$this->width_var*($i+1)-5,$this->graphheight-2, $colorLightBlue);
        }
    }
    function create_cloths()
    {
        $this->image=imagecreate($this->graphwidth+20,$this->graphheight+20);
    }
    function create_frame()
    {
        $this->get_var_wh();
        $colorBg=imagecolorallocate($this->image, $this->colorBg[0], $this->colorBg[1], $this->colorBg[2]);
        $colorGrey=imagecolorallocate($this->image, $this->colorGrey[0], $this->colorGrey[1], $this->colorGrey[2]);
        imageline($this->image, 0, 0, 0, $this->graphheight,$colorGrey);
        imageline($this->image, 0, 0, $this->graphwidth, 0,$colorGrey);
        imageline($this->image, ($this->graphwidth-1),0,($this->graphwidth-1),($this->graphheight-1),$colorGrey);
        imageline($this->image, 0,($this->graphheight-1),($this->graphwidth-1),($this->graphheight-1),$colorGrey);
    }
    function create_line()
     {
        $this->get_var_wh();
        $colorBg=imagecolorallocate($this->image, $this->colorBg[0], $this->colorBg[1], $this->colorBg[2]);
        $colorGrey=imagecolorallocate($this->image, $this->colorGrey[0], $this->colorGrey[1], $this->colorGrey[2]);
        $colorRed=imagecolorallocate($this->image, $this->colorRed[0], $this->colorRed[1], $this->colorRed[2]);
        for($i=1;$i<=$this->height_num;$i++)
         {
            $y1=($this->graphheight-($this->height_var/$this->height_max*$this->graphheight)*$i);
            $y2=($this->graphheight-($this->height_var/$this->height_max*$this->graphheight)*$i);
            imageline($this->image,0,$y1,$this->graphwidth,$y2,$colorGrey);
            imagestring($this->image,2,0,$this->graphheight-($this->height_var/$this->height_max*$this->graphheight)*$i,$this->height_var*$i,$colorRed);
         }
        unset($i);
        foreach($this->array_data[0] as $key=>$value)
        {
            imageline($this->image,$this->width_var*$i,0,$this->width_var*$i,$this->graphwidth,$colorGrey);
            imagestring($this->image,2,$this->width_var*$i,$this->graphheight-15,$key,$colorRed);
            $i++;
        }
    }
    function build($graph,$str_var)
    {
        header("Content-type: image/jpeg");
        $this->create_cloths();
        switch ($graph)
        {
            case "line":
                $this->create_frame();
                $this->create_line(); 
                $this->build_line($str_var); 
                break;
            case "rectangle":
                $this->create_frame();
                $this->build_rectangle($str_var); 
                $this->create_line();
                break;
        }
        imagepng($this->image);
        imagedestroy($this->image);
    }
}
?>
