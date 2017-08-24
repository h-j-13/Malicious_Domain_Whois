<template>
  <div id="checktype">
    <h1 style="font-weight: bold; font-size:45px;">{{urlData}}域名画像</h1>
    <p></p>
    <div class="tab1">
<!--       <h2>域名性质：{{illtype}}</h2>
      <h2>评估分数评估</h2> -->
      <h2 style="float: right; margin-right: 150px; font-size: 17px; margin-top: 9px;" v-show="ifShow">{{webScore}}%可疑</h2>
      <div style="width:140px;float:right;height: 20px;" v-show="!ifShow"></div>
      <h2 style="float: right;font-size: 24px; margin-right: 20px;">域名性质：{{illtype}}</h2>
      <br>
      <!-- 85%可疑和下面这个表是可以控制的 -->
      <el-table
      :data="scoreData"
      v-if = "ifShow"
      stripe
      style="width: 80%">
      <el-table-column
        prop="locateScore"
        label="空间一致性"
        >
      </el-table-column>
      <el-table-column
        prop="whoisScore"
        label="域名Whois信息健康性"
        >
      </el-table-column>
      <el-table-column
        prop="contentScore"
        label="内容合法性"
        >
      </el-table-column>
      <el-table-column
        prop="score"
        label="可疑程度"
        >
      </el-table-column>
    </el-table>
    </div>
  </div>
</template>
<script>
export default{
  data:function(){
    return{
      illtype:"",
      score:"",
      webScore:"",
      urlData:'',
      ifShow:true,
      scoreData:[{}]
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
        async :false,
        type:'GET',
        success:function (samedata) {
            this.illtype=samedata.base_info.area;
            this.scoreData[0]=samedata.base_info;
            this.webScore=samedata.base_info.score;
            if(samedata.base_info.score_status == 0){
              this.ifShow = false;
            }
            else{
              this.ifShow = true;
            }
        }.bind(this),
        error:function(){
            alert('获取数据失败！')
        },
    });
    }
  }
}
</script>
