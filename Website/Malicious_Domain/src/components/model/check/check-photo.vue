<template>
<div v-if= "Mes.seen == 'true'" >
  <div id='checkphoto'>
  		<h1 style="font-weight: bold;">页面快照</h1>
  		<div class='tab1'>
  			<h3>网页标题</h3>
  		</div>
  		<div class='tab2'>
  			<p>{{Mes.dnstitle}}</p>
  		</div>
  		<div class='tab1'>
  			<h3>页面内容关键词</h3>
  		</div>
  		<div class='tab2'>
  			<p>{{Mes.dnskey}}</p>
  		</div>
  		<img :src="ImgPath" width="700" height="300" />  
  	</div>
  </div>
</template>

<script>
	export default{
		data(){
			return{
				ImgPath:"",
				Mes:[],
				urlData:""
			}
		},
		mounted:function(){
			var aUrl = document.URL;
		    if(aUrl.indexOf("value=")!=-1){
		        var str = aUrl.split("value=");
		      }
		    this.urlData = str[1];
      		this.getIMG();
    	},
		methods:{
			getIMG:function(){
				$.ajax({
		        url:this.myURL+"/check?value="+this.urlData,
		        dataType:"json",
		        type:'GET',
		        async :false,
		        success:function (data) {
		            this.Mes=data.show_img;
		            this.ImgPath = data.show_img.img;
		        }.bind(this),
		        error:function(){
		            alert('获取数据失败！');
		        }
		    })
		}
	}
}
</script>