<template>
  <div>
    <div class="year-data">
            <div class="year-font">请选择定位的维度：</div>
            <el-select v-model="value" placeholder="请选择" style="margin-left:160px;" @change="handleCommand">
                <el-option  
                  v-for="item in years"
                  :label="item.label"
                  :value="item.value">
                </el-option>
          </el-select>
        </div>
    <h1 class="head">非法域名空间分布统计</h1>
    <div id="unknown">
      <span></span>
      <span class="num-class">{{unknown}}</span>
    </div>
    <div id="unknown">
      <span></span>
      <span class="num-class">{{ forein }}</span>
    </div>
    <div id="spa-map"></div>
  </div>
</template>
<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/map/js/china"
  let SpaMap;

  export default{
  //处理选项的变化将改变后的值传送到url中作为参数进行查询
  methods: {
  handleCommand(value) {
    $.ajax({
      url:this.myURL+"/stainfo/space/spaceinfo?value="+value,
      dataType:"json",
      type:'GET',
      success:function (result)
      { //返回的两个值
      this.unknown="未知地理信息的恶意域名数量为:"+result.unknow;
      this.forein="海外的恶意域名数量为:"+result.foreign;
      //地图填充
      var xValue=[];
      var yValue=[];
      var i=0;
      var len=result.info.length;
      for(i=0;i < len;i++)
        {
          xValue[i]=result.info[i].name;
          yValue[i]=result.info[i].value;
        }

      SpaMap.setOption({
        series: [{
          name: '恶意域名',
          data:(function(){
          var res=[];
          for (i = 0; i < len; i++)
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
      }.bind(this),

      error:function()
      {
      alert("访问服务器失败");
      }

    })
  }
  },
  data () {
  return{
  unknown:"",
  forein:"",

  years:[{
  value: '1',
  label: '按照whois信息查询'
  }, {
  value: '2',
  label: '按照邮编查询'
  }, {
  value: '3',
  label: '按照IP地址查询'
  }, {
  value: '4',
  label: '按照电话查询'
  }, {
  value: '5',
  label: '按照icp地址查询'
  }],
  value:''
  }
  },

  mounted() {
  SpaMap = echarts.init(document.getElementById('spa-map'));
  SpaMap.setOption({
  tooltip: {
  trigger: 'item'
  },
  legend: {
  orient: 'vertical',
  left: 'left',
  data:['恶意域名数量']
  },
  visualMap: {
  min: 0,
  max: 2500,
  left: 'left',
  top: 'bottom',
  text: ['高','低'],           // 文本，默认为数值文本
  },

  series: [{
  name: '恶意域名',
  type: 'map',
  layoutCenter: ['50%', '50%'],
  layoutSize: 900,
  mapType: 'china',
  roam: false,
  label: {
  normal: {
  show: true
  },
  emphasis: {
  show: true
  }
  },
  data:[]
  }]
  });
  SpaMap.on('click', function (params) {
    var city = params.name;
    alert(city+"的恶意域名数量为:"+params.value);
  });
  window.onresize = myChart.resize;
  },
  components: {}
  }
</script>

<style>
  #spa-map{
  margin-top: 30px;
  margin-left: 50px;
  width: 90%;
  height: 720px;
  }
  .head{
  color:#08a9f2;
  text-align:center;
  }
</style>
