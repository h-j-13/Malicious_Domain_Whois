<template>
	<div>
		<div id="signChart"></div>
		<div class="whois-line"></div>
		<div id="signPlan"></div>
	</div>
</template>

<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/theme/macarons.js";

  export default{
  mounted () {

  var signChart = echarts.init(document.getElementById('signChart'),'macarons');
  signChart.setOption({
  title: { text: '非法域名注册商分布图', x:'center' },
  tooltip: {},
  xAxis: {
  data: [],
  axisLabel:{
  interval:0,  //横轴的信息全部显示
  rotate:-15 //-15度角倾斜显示
  }
  },
  yAxis: {name:'数量/个'},
  series: [{
  name: '数量',
  type: 'bar',
  barWidth : 40,
  data: []
  }]
  });

  var signPlan = echarts.init(document.getElementById('signPlan'),'macarons');
  signPlan.setOption({
  title : {
     subtext:' ',
     x:'center'
      },
  tooltip : {
  trigger: 'item',
  formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
  x : 'right',
  data:[]
  },
  series : [
  {
  name:'非法域名注册商分布图',
  type:'pie',
  radius : '70%',
  label: {
  normal: {show: true},
  emphasis: {show: true }
  },
  center : ['50%', '50%'],
  data:[
  //  {value:180, name:'A'},
  //  {value:200,name:'B'}
  ]
  }]
  })

  window.onresize = signChart.resize;

  //AJAX

  $.ajax({
  url:this.myURL+"/stainfo/whois/whoissign",
  dataType:"json",
  type:'GET',
  success:function (result)
  {
  var xValue=new Array();
  var yValue=new Array();
  var i = 0;
  //将信息合并到一个数组里面
  for (i = 0; i < 10; i++)
    {
       xValue[i]=result.info[i].registrar;
       yValue[i]=result.info[i].num;
    }
    signChart.setOption
    ({
       xAxis:{
            data: xValue,
            name:'恶意注册人'
            },
       series: [{
            data:yValue
             }]
     });
     
      signPlan.setOption({
         legend: {data:xValue},
         series : [{
                 data:(function(){
                       var res=[];
                       for (i = 0; i < 10; i++)
                       {
                          res.push({
                           name:xValue[i],
                           value:yValue[i]
                        });  
                       }
                       return res;
                       })()
                }]   
      })
   }
});
  
  }
  }
</script>

<style>
#signChart{
	width: 50%;
	height: 700px;
	margin-top: 20px;
	margin-left: 10px;
	float: left;
}
	#signPlan{
		width: 50%;
		height: 700px;
		margin: 30px auto;
		float:left ;
	}
</style>
