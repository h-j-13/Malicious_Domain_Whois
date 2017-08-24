<template>
  <div>

    <h1 class="head">非法域名概览</h1>
    <div id="spa-map"></div>
    <div id="myPie"></div>

  <!-- 表格部分 -->
    <el-table
      :data="tableData"
      stripe
      @row-click='handleRowHandle'
      style="width: 100%">
      <el-table-column
        prop="province"
        label="省份"
        width="200">
      </el-table-column>
      <el-table-column
        prop="domain"
        label="域名"
        width="200"
        >
      </el-table-column>
      <el-table-column
        prop="name"
        label="注册人姓名"
        width="250"
        >
      </el-table-column>
      <el-table-column
        prop="nature"
        label="类型"
        width="250"
        >
      </el-table-column>
      <el-table-column
        prop="phone"
        label="注册电话"
        width="250"
        >
      </el-table-column>
      <el-table-column
        prop="score"
        label="可疑程度"
        width="150"
        >
      </el-table-column>
      <el-table-column
        prop="email"
        label="注册邮箱"
        width="250"
        >
      </el-table-column>
    </el-table>

    <div>
      <el-pagination
        @current-change="pageIndexChange"
        :current-page="currentPage"
        :page-size="10"
        layout="total, prev, pager, next, jumper"
        :total="allDomain">
      </el-pagination>
    </div>

  </div>
</template>
<script>
  import echarts from "echarts/lib/echarts";
  import "echarts/map/js/china"
  let SpaMap;
  export default{
    data(){
      return{
        badPie:'',
        tableData:[],
        currentPage:1,
        countryMap:[],
        allDomain:0,
        pieMap:[{"name":"合法域名","value":0},{"name":"非法域名","value":0}],
        mes:{
          country:'',
          page:''
        }
      }
    },
    mounted(){
      this.getMapData();
      
      this.getCountryData();
    },
    methods:{
      createMap:function(){
        var that = this;
        SpaMap = echarts.init(document.getElementById('spa-map'));
        var option = {
          tooltip: {
              trigger: 'item'
          },
          visualMap: {
              min: 0,
              max: 2500,
              left: 'left',
              top: 'bottom',
              text: ['高','低'],           // 文本，默认为数值文本
              calculable: true
          },
          series: [
              {
                  name: '非法域名',
                  type: 'map',
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
                  data:that.countryMap
              }
          ]
      };
      SpaMap.setOption(option);
      SpaMap.on('click', function (params) {
        that.mes.country = params.name;
        that.mes.page = params.value;
        that.currentPage = 1;
        that.getTable();
        that.createPie();
      });
      window.onresize = SpaMap.resize;
      },
      getMapData:function(){
        var that = this;
        $.ajax({
          url:this.myURL+"/countrycondition",
          dataType:"json",
          type:"GET",
          success:function(result){
            that.countryMap = result.domainNum;
            that.createMap();
            console.log(that.countryMap)
          }
        })
      },
      createPie:function(){
        var that = this;
        this.badPie = echarts.init(document.getElementById('myPie'));
        var option = {
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['合法域名','非法域名']
            },
            series : [
                {
                    name: '访问来源',
                    type: 'pie',
                    label:{
                      normal:{
                        show:false ,
                        position : 'outside'
                      },
                      emphasis:{
                        show :false,
                      }
                    },
                    radius : '80%',
                    center: ['50%', '60%'],
                    data:that.pieMap,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        this.badPie.setOption(option);
        window.onresize = this.badPie.resize;
      },
      getTable:function(){
        var that = this;
        $.ajax({
        url:this.myURL+"/provincecondition",
        data:{"province":that.mes.country,"page":1},
        dataType:"json",
        type:"GET",
        success:function(result)
        {
          that.tableData = result.provinceData;
          that.allDomain = result.provinceNum.allDomain;
          that.pieMap[0].value = result.provinceNum.allDomain -  result.provinceNum.maliciousDomain;
          that.pieMap[1].value = result.provinceNum.maliciousDomain;
          that.createPie();
        }
        //AJAX
        })
      },
      pageIndexChange:function(changePage){
        var that = this;
        $.ajax({
        url:this.myURL+"/provincecondition",
        data:{"province":that.mes.country,"page":changePage},
        dataType:"json",
        type:"GET",
        success:function(result)
        {
          that.tableData = result.provinceData;
        }
        //AJAX
        });
      },
      getCountryData:function(){
        this.mes.country = "全国",
        this.getTable();
      },
      handleRowHandle:function(row,event,column){
        this.$router.push({ path: '/check?value='+row.domain });
      }
    }
  }
</script>

<style>
  #spa-map{
  margin-top: 30px;
  margin-left: 50px;
  width: 75%;
  height: 720px;
  float: left;
  }
  #myPie{
  margin-top: 30px;
  margin-left: 50px;
  width: 15%;
  height: 520px;
  float: right;
  }
  .head{
  color:#08a9f2;
  text-align:center;
  }
</style>
