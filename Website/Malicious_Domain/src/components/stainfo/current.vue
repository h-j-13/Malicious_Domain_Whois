<template>
  <div>
    <div class="main-right">
      <!--     	<transition name="fade"> -->
      <div class="con-underline">
        <div class="dns-num">
          <span>当前恶意注册人总量为:</span>
          <span class="num-class">{{ dnsnum }}</span>
        </div>
      </div>
    </div>
    <div id="top"></div>
    <el-table
    :data="tableData3"
    height="250"
    border=""
    style="width: 100%">
      <el-table-column
        prop="name"
        label="恶意注册人姓名"
        style=" width:40%">
      </el-table-column>
      <el-table-column
        prop="baddomain"
        label="恶意注册域名数量"
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
  //ajax请求数据
  dnsnum:"",

  //表格的填充数据tableDate3：
  tableData3: [
  /*{
  Alldomain: '58',
  name: '王小虎',
  baddomain: '21'
  }*/
  ]}
  },
  //分页功能
  methods: {
  handleCurrentChange(q) {
  $.ajax({
  url:this.myURL+"/stainfo/people/peoplename?value="+ q ,
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
         baddomain:result.info[i].baddomain   //恶意的数量 
     }), 
      xValue[i]=result.info[i].name;
      kind[i]=result.info[i].Alldomain-result.info[i].baddomain;
      bad[i]=result.info[i].baddomain
  }  
  this.tableData3=res;
  //处理echarts
 
yearChart.setOption({
 xAxis: [{
  name:'姓名',
  data: xValue
  }],
 series: [
{
  name:'恶意域名数量',
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
  mounted () {
   yearChart = echarts.init(document.getElementById('top'),'macarons');
  yearChart.setOption({
  title: { text: '恶意注册人信息', x:'center' },
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
  data:['趋势走向','正常域名数量','恶意域名数量'],
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
  }],

  series: [{
  name:'恶意域名数量',
  type:'bar',
  stack: '域名数量',
  data:[],
  itemStyle:{
  normal:{color:'#08a9f2'}
  }},
  {name:'正常域名数量',
  type:'bar',
  stack: '域名数量',
  data:[],
  itemStyle:{
  normal:{color:'lightblue'}
  }},
  {
  name:'趋势走向',
  type:'line',
  data:[],
  itemStyle:{
  normal:{color:'white'}
  } }]
  });
  window.onresize=yearChart.resize;

  //ajax填充数据
  $.ajax({
  url:"http://172.29.152.3:8000/stainfo/people/peoplename?value=1",
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
  var len=result.info.length;
  var i = 0;
  for (i = 0; i < len; i++)
  {
     res.push({
         Alldomain:result.info[i].Alldomain,  //善意的数量
         name: result.info[i].name,
         baddomain:result.info[i].baddomain   //恶意的数量 
     }), 
      xValue[i]=result.info[i].name;
      kind[i]=result.info[i].Alldomain-result.info[i].baddomain;
      bad[i]=result.info[i].baddomain
  }  
  this.tableData3=res;
  //处理echarts
 
yearChart.setOption({
 xAxis: [{
  name:'姓名',
  data: xValue
  }],
 series: [
{
  name:'恶意域名数量',
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
  width: 95%;
  height: 300px;
  margin-left: 40px;
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
  body {
  background: #FFF;
  color: #000;
  font: normal normal 12px Verdana, Geneva, Arial, Helvetica, sans-serif;
  margin: 10px;
  padding: 0
  }

  table, td, a {
  color: #000;
  font: normal normal 12px Verdana, Geneva, Arial, Helvetica, sans-serif
  }

  h1 {
  font: normal normal 18px Verdana, Geneva, Arial, Helvetica, sans-serif;
  margin: 0 0 5px 0
  }

  h2 {
  font: normal normal 16px Verdana, Geneva, Arial, Helvetica, sans-serif;
  margin: 0 0 5px 0
  }

  h3 {
  font: normal normal 13px Verdana, Geneva, Arial, Helvetica, sans-serif;
  color: #008000;
  margin: 0 0 15px 0
  }

  div.tableContainer {
  clear: both;
  border: 1px solid #963;
  height: 285px;
  overflow: auto;
  width: 756px
  }


  html>body div.tableContainer {
  overflow: hidden;
  width: 756px
  }


  div.tableContainer table {
  float: left;
  width: 740px
  }

  html>body div.tableContainer table {
  width: 756px
  }


  thead.fixedHeader tr {
  position: relative
  }

  html>body thead.fixedHeader tr {
  display: block
  }

  /* make the TH elements pretty */
  thead.fixedHeader th {
  background: #C96;
  border-left: 1px solid #EB8;
  border-right: 1px solid #B74;
  border-top: 1px solid #EB8;
  font-weight: normal;
  padding: 4px 3px;
  text-align: left
  }


  thead.fixedHeader a, thead.fixedHeader a:link, thead.fixedHeader a:visited {
  color: #FFF;
  display: block;
  text-decoration: none;
  width: 100%
  }

  thead.fixedHeader a:hover {
  color: #FFF;
  display: block;
  text-decoration: underline;
  width: 100%
  }



  html>body tbody.scrollContent {
  display: block;
  height: 262px;
  overflow: auto;
  width: 100%
  }

  tbody.scrollContent td, tbody.scrollContent tr.normalRow td {
  background: #FFF;
  border-bottom: none;
  border-left: none;
  border-right: 1px solid #CCC;
  border-top: 1px solid #DDD;
  padding: 2px 3px 3px 4px
  }

  tbody.scrollContent tr.alternateRow td {
  background: #EEE;
  border-bottom: none;
  border-left: none;
  border-right: 1px solid #CCC;
  border-top: 1px solid #DDD;
  padding: 2px 3px 3px 4px
  }

  /* define width of TH elements: 1st, 2nd, and 3rd respectively.          */
  /* Add 16px to last TH for scrollbar padding. All other non-IE browsers. */
  /* http://www.w3.org/TR/REC-CSS2/selector.html#adjacent-selectors        */
  html>body thead.fixedHeader th {
  width: 200px
  }

  html>body thead.fixedHeader th + th {
  width: 240px
  }

  html>body thead.fixedHeader th + th + th {
  width: 316px
  }

  html>body tbody.scrollContent td {
  width: 200px
  }

  html>body tbody.scrollContent td + td {
  width: 240px
  }

  html>body tbody.scrollContent td + td + td {
  width: 300px
  }


</style>

