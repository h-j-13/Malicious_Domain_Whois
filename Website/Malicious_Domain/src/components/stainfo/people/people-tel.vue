<template>
	<div>
    <div class="main-right">
      <!--     	<transition name="fade"> -->
      <div class="con-underline">
        <div class="dns-num">
          <span>当前非法域名注册电话总量为:</span>
          <span class="num-class">{{ dnsnum }}</span>
        </div>
      </div>
      <!--     	</transition> -->
    </div>
    <div id="top"></div>
    <el-table
    :data="tableData3"
    height="250"
    border=""
    style="width: 100%">
      <el-table-column
        prop="name"
        label="非法注册电话"
        style=" width:40%">
      </el-table-column>
      <el-table-column
        prop="baddomain"
        label="非法注册域名数量"
        style=" width:30%">
      </el-table-column>
      <el-table-column
        prop="Alldomain"
        label="注册域名总数量">
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination
        @current-change="handleCurrentChange"
        v-on:current-change="pageIndexChange"
        :current-page="PageIndex"
        :page-size="10"
        layout="total, prev, pager, next, jumper"
        :total="1000">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/theme/macarons.js";
  var yearChart;
  export default{
  data () {
  return{
  dnsnum:"",
  //表格填充
  tableData3: []
  }
  },
  //分页
  methods: {
  handleCurrentChange(q) {
  $.ajax({
  url:this.myURL+"/stainfo/people/peopletel?value="+ q ,
  dataType:"json",
  type:'GET',
  success:function (result)
  { //原因：全局变量绑定,显示顶端的数字
  this.dnsnum =result.dnsnum;
  //表格填充
  var res=[];
  var xValue=[];
  var kind=[];
  var bad=[];
  var i = 0;
  var len=result.info.length;
  for (i = 0; i < len; i++)
  {
     res.push({
         Alldomain:result.info[i].Alldomain,  //善意的数量
         name: result.info[i].name,
         baddomain:result.info[i].baddomain   //非法的数量 
     }), 
      xValue[i]=result.info[i].name;
      kind[i]=result.info[i].Alldomain-result.info[i].baddomain;
      bad[i]=result.info[i].baddomain
  }  
  this.tableData3=res;
  //处理echarts
 
yearChart.setOption({
 xAxis: [{
  name:'电话',
  data: xValue
  }],
 series: [
{
  name:'非法域名数量',
  data:bad
 },
{
      name:'正常域名数量',
      data:kind
 },
 {
    name:'趋势走向',
    data:bad
 }
 ]
 });
  }.bind(this),
  error:function()
  {
  alert("访问服务器失败");
  }
  });

  }
  },
  //echarts数据
  mounted () {
  yearChart = echarts.init(document.getElementById('top'),'macarons');
  yearChart.setOption({
  title: { text: '非法注册电话信息', x:'center' },
  tooltip: {
  trigger: 'axis',
  axisPointer: {
  type: 'cross',
  crossStyle: {
  color: 'lightblue',
  }
  }
  },
  legend: {
  data:['趋势走向','正常域名数量','非法域名数量'],
  align: 'left',
  left: 20
  },
  xAxis: [
  {
  type: 'category',
  name:'姓名',
  data: [],
  axisPointer: {
  type: 'shadow'
  },
  axisLabel:{
  interval:0,  //横轴的信息全部显示
  rotate:-15 //-15度角倾斜显示
  }
  }
  ],
  yAxis: [
  {
  type: 'value',
  name: '域名数量/个',
  axisLabel: {
  formatter: '{value} '
  }
  },

  ],
  series: [
  {
  name:'非法域名数量',
  type:'bar',
  stack: '域名数量',
  data:[],
  itemStyle:{
  normal:{color:'#08a9f2'}
  }

  },
  {
  name:'正常域名数量',
  type:'bar',
  stack: '域名数量',
  data:[],
  itemStyle:{
  normal:{color:'lightblue'}
  }
  },
  {
  name:'趋势走向',
  type:'line',
  data:[],
  itemStyle:{
  normal:{color:'white'}
  }

  }
  ]
  });
  window.onresize = yearChart.resize;
  //ajax填充数据
  $.ajax({
  url:"http://172.29.152.3:8000/stainfo/people/peopletel?value=1",
  dataType:"json",
  type:'GET',
  success:function (result)
  { 
  //原因：全局变量绑定,显示顶端的数字
  this.dnsnum =result.dnsnum;
  //表格填充
  var res=[];
  var xValue=[];
  var kind=[];
  var bad=[];
  var i = 0;
  var len=result.info.length;
  for (i = 0; i < len; i++)
  {
     res.push({
         Alldomain:result.info[i].Alldomain,  //善意的数量
         name: result.info[i].name,
         baddomain:result.info[i].baddomain   //非法的数量 
     }), 
      xValue[i]=result.info[i].name;
      kind[i]=result.info[i].Alldomain-result.info[i].baddomain;
      bad[i]=result.info[i].baddomain
  }  
  this.tableData3=res;
  //处理echarts
 
yearChart.setOption({
 xAxis: [{
  name:'电话',
  data: xValue
  }],
 series: [
{
  name:'非法域名数量',
  data:bad
 },
{
      name:'正常域名数量',
      data:kind
 },
 {
    name:'趋势走向',
    data:bad
 }
 ]
 });
  }.bind(this),
  error:function()
  {
  alert("访问服务器失败");
  }
  });

  }
  }

</script>

<style>
  #top{
  width: 95%;
  height: 420px;
  margin-left: 20px;
  margin-top: 0px;
  margin-bottom: 20px;
  border-bottom: 1px solid #cccccc;
  }
  #left{
  width: 42%;
  height: 300px;
  margin-left: 40px;
  float: left;
  }
  .main-right{
  -webkit-box-flex:5;
  -ms-flex:5.5;
  flex:5;
  padding: 20px 40px;
  }
  .con-underline{
  border-bottom: 1px solid #CCCCCC;
  height: 40px;
  }
  .dns-num{
  border-left: 8px solid #72b16a;
  }
  .dns-num span{
  padding-left: 15px;
  color: #72b16a;
  }
  .num-class{
  padding-left:5px!important;
  color: orange!important;
  }

</style>
