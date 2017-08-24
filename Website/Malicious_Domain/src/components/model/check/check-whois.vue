<template>
	<div id='checkwhois'>
		<h1 style="font-weight: bold;">域名WHOIS信息</h1>
    <el-table
		 :data="whoisData"
		 style="width: 100%">
	    <el-table-column
			 	prop="name"
			 	label="名称">
		 	</el-table-column>
	    <el-table-column
				prop="info"
				label="内容">
			</el-table-column>
    </el-table>
  </div>
</template>
<script>
	export default{
		data(){
			return{
				whoisData: [],
				urlData:''
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
	            this.whoisData = data.whois
	        }.bind(this),
	        error:function(){
	            alert('获取数据失败！')
	        },
	    });
		}
	}
	}
</script>
