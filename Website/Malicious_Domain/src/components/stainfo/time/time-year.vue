<template>
	<div>
    <h1 class="head">
      <span class="head">{{num}}</span>
      年创建/到期域名展示
    </h1>
		<div class="year-data">
			<div class="year-font">请选择查看年份：</div>
			<el-select v-model="value" placeholder="请选择" style="margin-left:130px;" @change="handleCommand">
			    <el-option
			      v-for="item in years"
			      :label="item.label"
			      :value="item.value">
			    </el-option>
		  </el-select>
		</div>
		<div id="year-top">	
		</div>
    <h2 class="bing">
      2003-
      <span >{{num}}</span>
      创建/到期域名展示
    </h2>
		<div id="year-left"></div>
		<div class="year-line"></div>
		<div id="year-right"></div>
	</div>
</template>

<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/theme/macarons.js";
  var leftChart;
  var rightChart;
  var yearChart
  export default{
  data () {
  return{
  num:'',
  years:[{
  value: '2007',
  label: '2007'
  }, {
  value: '2008',
  label: '2008'
  }, {
  value: '2009',
  label: '2009'
  }, {
  value: '2010',
  label: '2010'
  }, {
  value: '2011',
  label: '2011'
  },
  {
  value: '2012',
  label: '2012'
  },
  {
  value: '2013',
  label: '2013'
  },
  {
  value: '2014',
  label: '2014'
  },
  {
  value: '2015',
  label: '2015'
  },
  {
  value: '2016',
  label: '2016'
  }],
  value:''
  }
  },

  //处理选项的变化将改变后的值传送到url中作为参数进行查询
  methods: {
  handleCommand(value) {
  $.ajax({
  url:this.myURL+"/stainfo/time/timeyear?value="+value,
  dataType:"json",
  type:'GET',
  success:function (result)
  {
  //返回value值作为饼图和最上面的大标题的题目
  this.num=value;
  var year=[];
  var end=[];
  var cre=[];
  var cValue=[];
  var eValue=[];
  var i=0;
  var len=result.e_date.length;
  //12个月的两个y值
  for(i=0;i< 12;i++)
   {
     cValue[i]=result.year[i].cValue;
     eValue[i]=result.year[i].eValue;
   }
   for(i=0;i< len;i++)
   {
     year[i]=result.e_date[i].name;
     end[i]=result.e_date[i].value;
     cre[i]=result.c_date[i].value;
   }
  //top的折线图
  yearChart.setOption({
  series: [{
  name: '创建域名',
  type: 'line',
  data: cValue
  },{
  name: '到期域名',
  type: 'line',
  data: eValue
  }]
  });
  //left的饼图
  rightChart.setOption({
  legend: {data:year},
  series : [{
  data:(function(){
  var res=[];
  for (i = 0; i < len; i++)
                       {
                          res.push({
                           name:year[i],
                           value:end[i]
                           });  
                       }
                       return res;
                       })()
                }]   
      })
  //right的饼图
  leftChart.setOption({
  legend: {data:year},
  series : [{
  data:(function(){
         var res=[];
         for (i = 0; i < len; i++)
                       {
                          res.push({
                           name:year[i],
                           value:cre[i]
                           });  
                       }
                       return res;
                       })()
                }]   
      })
  }.bind(this)
  })
  }
  },
  mounted () {
  yearChart = echarts.init(document.getElementById('year-top'),'macarons');
  yearChart.setOption({
  legend: {                                 
  padding: 5,                             
  itemGap: 10,                           
  data: ['创建域名', '到期域名'],
  x:'left'
  },
  tooltip: {},
  xAxis: {
  name:"月份",
  data: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
  },
  yAxis: {name:'数量'},
  series: [{
  name: '创建域名',
  type: 'line',
  data: []
  },{
  name: '到期域名',
  type: 'line',
  data: []
  }]
  });
  leftChart = echarts.init(document.getElementById('year-left'),'macarons');
  leftChart.setOption({
  tooltip : {
  trigger: 'item',
  formatter: "{a} <br/>{b} : {c} ({d}%)"
           },
           legend: {
           x : 'center',
           y : 'bottom',
           data:[]
           },

           series : [
           {
           name:'半径模式',
           type:'pie',
           radius : '70%',
           center : ['50%', '50%'],
           roseType : 'radius',
           data:[],
           label: {
           normal: {show: false},
           emphasis: {show: true }
           },
           }
           ]
           });

           rightChart = echarts.init(document.getElementById('year-right'),'macarons');
           rightChart.setOption({

           tooltip : {
           trigger: 'item',
           formatter: "{a} <br/>{b} : {c} ({d}%)"
           },
           legend: {
           x : 'center',
           y : 'bottom',
           data:[]
           },
           series : [
           {
           name:'半径模式',
           type:'pie',
           radius : '70%',
           center : ['50%', '50%'],
           roseType : 'radius',
           data:[ ],
           label: {
           normal: {show: false},
           emphasis: {show: true }
           },
           }
           ]
           })
           window.onresize = yearChart.resize;

           }
           }
         </script>

<style>
  .year-data{
  margin-left: 20px;
  margin-top: 20px;
  margin-bottom: 10px;
  height: 40px;

  position: relative;
  }
  .year-font{
  position: absolute;
  display: inline-block;
  top:6px;

  }
  #year-top{
  width: 95%;
  height: 420px;
  margin-left: 20px;
  margin-top: 0px;
  margin-bottom: 20px;
  border-bottom: 1px solid #cccccc;
  }
  #year-left{
  width: 42%;
  height: 300px;
  margin-left: 40px;
  float: left;
  }
  .year-line{
  height: 300px;
  margin-left: 20px;
  width: 1px;
  border-left: 1px solid #cccccc;
  float: left;
  }
  #year-right{
  width: 42%;
  height: 300px;
  margin-left: 20px;
  float: left;
  }
  .head{
  color:#08a9f2;
  text-align:center;
  }
  .bing{
  color:#08a9f2;
  text-align:center;
  }
</style>