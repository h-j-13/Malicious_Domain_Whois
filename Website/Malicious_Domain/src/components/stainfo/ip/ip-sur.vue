<template>
	<div>
		<div id="surChart" v-if="ifShow"></div>
    <div v-if="ifShow == false" class="ip-laoding2">
        <div class="spinner">
        <div class="spinner-container container1">
          <div class="circle1"></div>
          <div class="circle2"></div>
          <div class="circle3"></div>
          <div class="circle4"></div>
        </div>
        <div class="spinner-container container2">
          <div class="circle1"></div>
          <div class="circle2"></div>
          <div class="circle3"></div>
          <div class="circle4"></div>
        </div>
        <div class="spinner-container container3">
          <div class="circle1"></div>
          <div class="circle2"></div>
          <div class="circle3"></div>
          <div class="circle4"></div>
        </div>
      </div>
      </div>
  	</div>
</template>

<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/theme/macarons.js";

  export default{
  data(){
    return{
      ifShow:false,
      result:{}
    }
  },
  mounted () {
    this.runAjax();
  },
  updated () {
    this.runDom();
  },
  methods:{
    runAjax:function(){
      var that = this;
      $.ajax({
        url:this.myURL+"/stainfo/ip/ipsur",
        dataType:"json",
        type:'GET',
        success:function (result)
        {
          that.ifShow = true;
          that.result = result;
         }
      });
    },
    runDom:function(){
        var result = this.result;
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
           
          var surChart = echarts.init(document.getElementById('surChart'),'macarons');
          surChart.setOption({
          title: { text: '非法域名IP更新频率', x:'center' },
          tooltip: {},
          xAxis: {
          data: [],
          name:'天',
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
        // alert("1");
        surChart.setOption({
           xAxis:{
                 data: xValue1,
                 },
           series: [{
                name: '数量',
                type: 'bar',
                barWidth : 40,
                data:yValue
                 }]
         });

    window.onresize = surChart.resize;

    }
  }
	}
</script>

<style>
	#surChart{
		width: 95%;
		height: 700px;
		margin-top: 30px;
		margin-left: 30px;
	}
  .ip-laoding2{
    width: 100%;
    height:100%;
  }
</style>