<template>
	<div>
		<div id="upChart"></div>
	</div>
</template>

<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/theme/macarons.js";

  export default{
  mounted () {
  var upChart = echarts.init(document.getElementById('upChart'),'macarons');
  upChart.setOption({
  title: { text: 'Whois信息更新时间频率图', x:'center' },
  tooltip: {},
  xAxis: {
  name:'天',
  axisLabel:{
  interval:0,  //横轴的信息全部显示
  rotate:-15 //-15度角倾斜显示
  },
  data: []
  },
  yAxis: {
  name:'数量/个'},
  series: [{
  name: '数量',
  type: 'bar',
  barWidth : 40,
  data: []
  }]
  });
  window.onresize = upChart.resize;

  //ajax后台处理数据
  $.ajax({
  url:this.myURL+"/stainfo/time/updatefrequency",
  dataType:"json",
  type:'GET',
  success:function (result)
  {
  var xValue=new Array();
  var yValue=new Array();
  var xValue1=[];
  var i = 0;
  var len =result.info.length;
  //将信息合并到一个数组里面
  for (i = 0; i < len; i++)
    {
       xValue[i]=result.info[i].x;
       yValue[i]=result.info[i].y;
    }
  //处理x轴信息，使其显示为一个区间段
  for(i=0;i< len-1;i++)
  {
     xValue1[i]=xValue[i]+'~'+xValue[i+1];
  }
     xValue1[len-1]='>'+xValue[len-1];
    upChart.setOption
    ({
       xAxis:{
             data: xValue1,
             },
       series: [{
            name: '数量',
            type: 'bar',
            barWidth :40,
            data:yValue
             }]
     });
   }
});
        }
	}
</script>

<style>
	#upChart{
		width: 95%;
		height: 700px;
		margin-top: 30px;
		margin-left: 30px;
	}
</style>