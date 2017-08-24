<template>
	<div>
		<div id="IP-num1">
		</div>
		<div class="IP-line"></div>
		<div id="IP-num2">
		</div>
		<div style="clear:both"></div>
	</div>
	
</template>

<script>
	import echarts from "echarts/lib/echarts";
	import "echarts/theme/macarons.js";
	export default{
		data () {
			return{

			}
		},
		mounted () {
			var num1Chart = echarts.init(document.getElementById('IP-num1'),'macarons');
            num1Chart.setOption({
                title: { text: '当前非法域名在线IP与离线IP数量显示', x:'center' },
                tooltip: {},
                xAxis: {
                    data: ["Online","Offline"]
                },
                yAxis: {name:'数量/个'},
                series: [{
                    name: '状态',
                    type: 'bar',
                    barWidth : 80,
                    data: []
                }]
            });

            var num2Chart = echarts.init(document.getElementById('IP-num2'),'macarons');
            num2Chart.setOption({
            	  title : {
			        text: '比例视图',
			        x:'center'
			    },
			    tooltip : {
			        trigger: 'item',
			        formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
  x : 'center',
  y : 'bottom',
  data:["Online","Offline"]
  },

  series : [
  {
  name:'比例展示',
  type:'pie',
  radius : '55%',
  center : ['50%', '50%'],
  // roseType : 'radius',
  data:[]
  }
  ]
  })
  window.onresize = num1Chart.resize;


  $. ajax({
  url:"/static/ipnum.txt",
  dataType:"json",
  type:"GET",
  success:function(result)
  {
  //alert("Hi");
  var yValue=[];
  var xValue=["Online","Offline"]
  var i=0;
  yValue[0]=result.Offline;
  yValue[1]=result.Online;

  num1Chart.setOption({
  series: [{
  name: '数量',
  data: yValue
  }]
  });
  num2Chart.setOption({
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

  //SUCCEESS
  }
  //AJAX
  })

  }
  }
</script>

<style>
	#IP-num1{
		margin-top: 80px;
		width: 52%;
		height: 600px;
		float: left;
	}
	.IP-line{
		height: 600px;
		float: left;
		margin-left: 30px;
		width: 5px;
		margin-top: 80px;
		border-left: 1px solid #cccccc;
	}
	#IP-num2{
		margin-top: 80px;
		width: 42%;
		height: 600px;
		float: left;
	}
</style>