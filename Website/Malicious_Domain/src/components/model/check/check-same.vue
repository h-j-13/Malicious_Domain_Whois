<template>
	<div id='checksame' v-if="seenx == 'true'">
		<h1 style="font-weight: bold;">近期同类型事件分析</h1>
    <div class='tab1'>
      <h3>非法类型</h3>
    </div>
    <div class='tab2'>
      <p>{{sametype}}</p>
    </div>
    <div class='tab1'>
      <h3>同类型事件数量</h3>
    </div>
    <div class='tab2'>
      <p>{{samenum}}</p>
    </div>
    <div class='tab1'>
      <h3>事件类型趋势</h3>
    </div>
    <div class='tab1'>
      <div id="typego"></div>
    </div>
  </div>
</template>
<script>
import echarts from "echarts/lib/echarts";
import "echarts/theme/macarons.js";

	export default{
		data(){
			return{
		        sametype:'',
		        samenum:'',
		        seenx:'true',
		        urlData:"",
			}
		},
		ready:function(){

		},
    mounted () {
    		var aUrl = document.URL;
		    if(aUrl.indexOf("value=")!=-1){
		        var str = aUrl.split("value=");
		      }
		      this.urlData = str[1];
		      
			function showsame(samedata) {
	      	var sum = 0 ;
	        var dataFir = [];
	        var dataSec = [];
	        var dataThr = [];
	        var i = 0;
					var aree,typp,numm;
	        for(i = 0;i<samedata.xsame.length;i++)
	        {
	          var vall,namm;
	          namm = samedata.xsame[i].x;
	          vall = samedata.xsame[i].y;
	          dataFir[i] = namm;
	          dataSec[i] = vall;
	        }
	        aree = samedata.malicious_info[0].area;
	        typp = samedata.sametype;
	        numm = samedata.samenum;

					var Typegoing = echarts.init(document.getElementById('typego'),'macarons');
		            Typegoing.setOption({
		                title: { text: '同类事件趋势', x:'center' },
					    legend: {                                   // 图例配置
					        padding: 5,                             // 图例内边距，单位px，默认上下左右内边距为5
					        itemGap: 10,                            // Legend各个item之间的间隔，横向布局时为水平间隔，纵向布局时为纵向间隔
					        data: aree,
					        x:'left'
					    },
		          tooltip: {},
		              toolbox: {
					        show : true,
					        feature : {
					            mark : {show: true},
					            dataView : {show: true, readOnly: false},
					            magicType : {show: true, type: ['bar', 'line']},
					            restore : {show: true},
					            saveAsImage : {show: true}
					        }
					    },
					    calculable : true,
		                xAxis: {
		                    data :dataFir
		                },
		                yAxis: {},
		                series: [{
		                    name: aree,
		                    type: 'line',
		                    data: dataSec
		                }]
		            });
		      	}
            //window.onresize = myChart.resize;
						$.ajax({
								url:this.myURL+"/check?value="+this.urlData,
								dataType:"json",
								async :false,
								type:'GET',
								//date:{"name":123},
								success:function (samedata) {
										this.sametype=samedata.same_event[0].samet;
										this.samenum=samedata.same_event[0].samen;
										this.seenx=samedata.same_event[0].seen;
										showsame(samedata.same_event[0]);
								}.bind(this),
								error:function(){
										alert('获取数据失败！')
								},
						});
          }
	}
</script>
<style>
#typego{
		//margin-top: 30px;
		width: 760px;
		height: 320px;
}
</style>
