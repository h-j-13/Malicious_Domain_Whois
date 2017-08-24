<template>
  <div id='checkpower'>
    <div v-if="Pow.seen == 'true'">
      <div class='tab1'>
        <h3>权威网站检测结果</h3>
      </div>
      <div class='tab2'>
        <p>{{Pow.dnsanay}}</p>
      </div>
      <div class='tab1'>
        <h3>注册者信息</h3>
      </div>
      <div class='tab2'>
        <el-table
       :data="Pow.powerData"
       style="width: 100%">
          <el-table-column
          prop="powername"
          label="名称"></el-table-column>
          <el-table-column
          prop="powerinfo"
          label="内容"></el-table-column>
        </el-table>
      </div>
      <div class='tab1'>
        <h3>域名影响力热度</h3>
      </div>
      <div class='tab2'>
        <p>{{Pow.dnshot}}</p>
      </div>
      <div class='tab1'>
        <h3>域名排名&趋势</h3>
      </div>
      <div class='tab2'>
        <p>{{Pow.dnsno}}</p>
      </div>
      <div class='tab1'>
        <h3>在网络上出现的位置</h3>
      </div>
      <div class='tab2'>
        <p>{{Pow.dnsloc}}</p>
      </div>
      <div class='tab1'>
        <h3>包含的非法链接与分类</h3>
      </div>
      <div class='tab2'>
        <p v-for="item in Pow.newHerf">
          {{item}}
        </p>
      </div>
    </div>
  </div>
</template>
<script>
  export default{
    data(){
      return{
        Pow:[],
        urlData:"",
        testData:"this is\r\na test!"
      }
    },
    mounted:function(){
    var aUrl = document.URL;
    if(aUrl.indexOf("value=")!=-1){
        var str = aUrl.split("value=");
      }
      this.urlData = str[1];
      this.getData();
    },
    methods:{
      getData:function(){
      $.ajax({
          url:this.myURL+"/check?value="+this.urlData,
          dataType:"json",
          type:'GET',
          async :false,
          success:function (data) {
              this.Pow=data.analysis[0];
              this.Pow.newHerf=this.Pow.dnsherf.split("||");
          }.bind(this),
          error:function(){
              alert('获取数据失败！')
          },
      });
    }
    }
  }
</script>
<style>
.tab1{
  margin-left: 10px;
}
.tab2{
  margin-left: 40px;
}
</style>