<template>
	<div>
		<div id="signChart"></div>
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
  title: { text: '非法域名覆盖顶级域', x:'center' },
  tooltip: {},
  xAxis: {
  //data: ["A","B","C","D","E","F","G","H","I","J"]
  data:[],
  name:'恶意域名',
  axisLabel:{
  interval:0,  //横轴的信息全部显示
  rotate: -30  //横轴信息倾斜30度显示
  }
  },
  yAxis: {name:'数量/个'},
  series: [{
  name: '数量',
  type: 'bar',
  barWidth : 40,
  // data: [180, 170, 98, 96, 92, 87, 87, 64, 57, 49,]
  data:[]
  }]
  });

  var signPlan = echarts.init(document.getElementById('signPlan'),'macarons');
  signPlan.setOption({
  title : {
  x:'center'
  },
  tooltip : {
  trigger: 'item',
  formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
  orient : 'vertical',
  x : 'right',
  data: []
  },
  series : [
  {
  type:'pie',
  radius : '70%',
  center : ['50%', '50%'],
  label:{
  normal:{show:true},
  emphasis:{show:true}
  },
  data:[]
  }
  ]
  })
  window.onresize = signChart.resize;

  //ajax获取信息填充到echarts里面
  $.ajax({
  url:this.myURL+"/stainfo/whois/whoisdomains",
  dataType:"json",
  type:'GET',
  success:function (result)
  {
  var xValue=new Array();
  var yValue=new Array();
  var i = 0;
  var len=result.info.length;
  //将信息合并到一个数组里面
  for (i = 0; i < len; i++)
    {
       xValue[i]=result.info[i].tld;
       yValue[i]=result.info[i].num;
    }
    signChart.setOption
    ({
       xAxis:{
            data: xValue,
             name:'非法注册域名'
             },
       series: [{
            name: '数量',
            type: 'bar',
            barWidth : 40,
            data:yValue
             }]
     });
      signPlan.setOption({
         legend: {
           data:xValue,
                  },
        series : [{
                 data:(function(){
                       var res=[];
                       for (i = 0; i < 9; i++)
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
  width: 95%;
  height: 500px;
  margin-left: 20px;
  margin-top: 0px;
  margin-bottom: 20px;
  border-bottom: 1px solid #cccccc;

}
	#signPlan{
		width: 50%;
		height: 700px;
		margin-top: 20px;
		margin-left: 20px;
		float:left ;
	}
</style>
