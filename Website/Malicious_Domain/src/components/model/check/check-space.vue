<template>
  <div id='checkspace'>
	<h1 style="font-weight: bold;">位置信息</h1>
    <div id="checkmap"></div>
  </div>
</template>
<script>
    import echarts from "echarts/lib/echarts";
    import "echarts/map/js/china"


    export default{
      data () {
        return{
        	urlData:''
        }
      },
        methods: {
        },
        mounted() {
        	var aUrl = document.URL;
		    if(aUrl.indexOf("value=")!=-1){
		        var str = aUrl.split("value=");
		      }
		    this.urlData = str[1];
        	$.ajax({
		        url:this.myURL+"/check?value="+this.urlData,
		        async :false,
		        dataType:"json",
		        type:'GET',
		        success:function (ajaxdata) {
		            var data=ajaxdata.position;
		            var geoCoordMap = ajaxdata.geoCoordMap;
					function convertData(data) {
					 var res = [];
					 for (var i = 0; i < data.length; i++) {
							 var geoCoord = geoCoordMap[data[i].name];
							 if (geoCoord) {
									 res.push({
											 name: data[i].name,
											 value: geoCoord.concat(data[i].value)
									 });
							 }
					 }
					 return res;
					};
					function randomValue() {
						return Math.round(Math.random()*1000);
					}
            let CheckMap = echarts.init(document.getElementById('checkmap'));
            CheckMap.setOption({
						    tooltip: {},
						    // visualMap: {
						    //     min: 0,
						    //     max: 1500,
						    //     left: 'left',
						    //     top: 'bottom',
						    //     text: ['High','Low'],
						    //     seriesIndex: [1],
						    //     inRange: {
						    //         color: ['#e0ffff', '#006edd']
						    //     },
						    //     calculable : true
						    // },
						    geo: {
						        map: 'china',
						        roam: true,
						        label: {
						            normal: {
						                show: true,
						                textStyle: {
						                    color: 'rgba(0,0,0,0.4)'
						                }
						            }
						        },
						        itemStyle: {
						            normal:{
						                borderColor: 'rgba(0, 0, 0, 0.2)'
						            },
						            emphasis:{
						                areaColor: null,
						                shadowOffsetX: 0,
						                shadowOffsetY: 0,
						                shadowBlur: 20,
						                borderWidth: 0,
						                shadowColor: 'rgba(0, 0, 0, 0.5)'
						            }
						        }
						    },
						    series : [
						       {
						           type: 'scatter',
						           coordinateSystem: 'geo',
						           data: convertData(data),
						           symbolSize: 10,
						           symbolRotate: 5,
						           label: {
						               normal: {
						                   formatter: '{b}',
						                   position: 'right',
						                   show: false
						               },
						               emphasis: {
						                   show: true
						               }
						           },
						           itemStyle: {
						               normal: {
						                    color: 'red'
						               }
						           }
						        },
						        {
						            type: 'map',
						            geoIndex: 0,
						            // tooltip: {show: false},
						            data:[
						                {name: '北京'},
						                {name: '天津'},
						                {name: '上海'},
						                {name: '重庆'},
						                {name: '河北'},
						                {name: '河南'},
						                {name: '云南'},
						                {name: '辽宁'},
						                {name: '黑龙江'},
						                {name: '湖南'},
						                {name: '安徽'},
						                {name: '山东'},
						                {name: '新疆'},
						                {name: '江苏'},
						                {name: '浙江'},
						                {name: '江西'},
						                {name: '湖北'},
						                {name: '广西'},
						                {name: '甘肃'},
						                {name: '山西'},
						                {name: '内蒙古'},
						                {name: '陕西'},
						                {name: '吉林'},
						                {name: '福建'},
						                {name: '贵州'},
						                {name: '广东'},
						                {name: '青海'},
						                {name: '西藏'},
						                {name: '四川'},
						                {name: '宁夏'},
						                {name: '海南'},
						                {name: '台湾'},
						                {name: '香港'},
						                {name: '澳门'}
						            ]
						        }
						    ]
						});
				        }.bind(this),
				        error:function(){
				            alert('获取数据失败！');
				        }
				    })

        //window.onresize = myChart.resize;
        },
    }
</script>

<style>
#checkmap{
		//margin-top: 30px;
		//margin-left: 50px;
		width: 560px;
		height: 420px;
}

</style>
