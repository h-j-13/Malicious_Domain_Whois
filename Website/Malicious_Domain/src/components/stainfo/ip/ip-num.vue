<template>
  <div>
    <div id="IP-num1"  v-if="ifShow">
    </div>
    <div v-if="ifShow == false" class="ip-laoding">
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
    <div class="IP-line"></div>
    <div id="IP-num2" v-if="ifShow">
    </div>
      <div v-if="ifShow == false" class="ip-laoding">
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
    <div style="clear:both"></div>
  </div>
  
</template>

<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/theme/macarons.js";
  export default{
    data () {
      return{
        ifShow:false,
        result:{}
      }
    },
    mounted() {
        this.getData();
    },
    updated(){
        this.runDemo();
    },
    methods:{
      getData:function(){
        var that = this;
        $. ajax({
        url:this.myURL+"/stainfo/ip/ipnum",
        dataType:"json",
        type:"GET",
        success:function(result)
        {
          that.ifShow = true;
          that.result = result;
        }
        //AJAX
        })
      },
      runDemo:function(){
        var result = this.result;
        var yValue=[];
        var xValue=["Online","Offline"]
        var i=0;
        yValue[0]=result.Offline;
        yValue[1]=result.Online;

        var num1Chart = echarts.init(document.getElementById('IP-num1'),'macarons');
        var num2Chart = echarts.init(document.getElementById('IP-num2'),'macarons');
        num1Chart.setOption({
            title: { text: '当前非法域名在线IP与离线IP数量显示', x:'center' },
            tooltip: {},
            xAxis: {
                data: ["Online","Offline"]
            },
            yAxis: {},
            series: [{
                name: '状态',
                type: 'bar',
                barWidth : 80,
                data: []
            }]
        });

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
        for (i = 0; i < 2; i++)
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

         window.onresize = num1Chart.resize;
      }
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
  .spinner {
  margin: 240px auto;
  width: 200px;
  height: 200px;
  position: relative;
}
.container1 > div, .container2 > div, .container3 > div {
  width: 30px;
  height: 30px;
  background-color: #333;
 
  border-radius: 100%;
  position: absolute;
  -webkit-animation: bouncedelay 1.2s infinite ease-in-out;
  animation: bouncedelay 1.2s infinite ease-in-out;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}
 
.spinner .spinner-container {
  position: absolute;
  width: 100%;
  height: 100%;
}
 
.container2 {
  -webkit-transform: rotateZ(45deg);
  transform: rotateZ(45deg);
}
 
.container3 {
  -webkit-transform: rotateZ(90deg);
  transform: rotateZ(90deg);
}
 
.circle1 { top: 0; left: 0; }
.circle2 { top: 0; right: 0; }
.circle3 { right: 0; bottom: 0; }
.circle4 { left: 0; bottom: 0; }
 
.container2 .circle1 {
  -webkit-animation-delay: -1.1s;
  animation-delay: -1.1s;
}
 
.container3 .circle1 {
  -webkit-animation-delay: -1.0s;
  animation-delay: -1.0s;
}
 
.container1 .circle2 {
  -webkit-animation-delay: -0.9s;
  animation-delay: -0.9s;
}
 
.container2 .circle2 {
  -webkit-animation-delay: -0.8s;
  animation-delay: -0.8s;
}
 
.container3 .circle2 {
  -webkit-animation-delay: -0.7s;
  animation-delay: -0.7s;
}
 
.container1 .circle3 {
  -webkit-animation-delay: -0.6s;
  animation-delay: -0.6s;
}
 
.container2 .circle3 {
  -webkit-animation-delay: -0.5s;
  animation-delay: -0.5s;
}
 
.container3 .circle3 {
  -webkit-animation-delay: -0.4s;
  animation-delay: -0.4s;
}
 
.container1 .circle4 {
  -webkit-animation-delay: -0.3s;
  animation-delay: -0.3s;
}
 
.container2 .circle4 {
  -webkit-animation-delay: -0.2s;
  animation-delay: -0.2s;
}
 
.container3 .circle4 {
  -webkit-animation-delay: -0.1s;
  animation-delay: -0.1s;
}
 
@-webkit-keyframes bouncedelay {
  0%, 80%, 100% { -swebkit-transform: scale(0.0) }
  40% { -webkit-transform: scale(1.0) }
}
 
@keyframes bouncedelay {
  0%, 80%, 100% {
    transform: scale(0.0);
    -webkit-transform: scale(0.0);
  } 40% {
    transform: scale(1.0);
    -webkit-transform: scale(1.0);
  }
}
.ip-laoding{
  width: 42%;
  height: 500px;
  float: left;
}
</style>