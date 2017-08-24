<template>
	<main>
		<div id="model-container">
			<div class="model-top">
				<div class="con-underline">
					<div class="dns-num">
						<span>当前非法域名数量：</span> <span class="num-class">{{ dnsnum }}</span>
					</div>
				</div>
				<router-view></router-view>
			</div>
			<div id="inp">
			<div class="search-logo">
				<img src="../../assets/slogo.png" height="125" width="210">
			</div>
			<form>
		  		<el-input placeholder="请输入域名"  v-model="inputs">
		    	<el-button slot="append" icon="search" @click="onSubmit">确定</el-button>
		  		</el-input>
		  	</form>
			</div>
		</div>
	</main>
</template>

<script>
	export default{
		data(){
			return{
				dnsnum:3000
			}
		},
		mounted(){
		var that = this;
		$.ajax({
	        url:this.myURL+"/homepage",
	        dataType:"json",
	        type:'GET',
	        success:function (result)
	        {
	          that.dnsnum = result.num;
	         }
	      });
		},
		methods: {
      	onSubmit:function() {
      		this.$router.push({ path: '/check?value='+this.inputs });
		  }
      }
    }
</script>

<style>
#inp{
	width: 40%;
	height: 20%;
	margin: auto auto;
	margin-top: 15%;
	text-align: center;
}
.search-logo{
	margin-top: -145px;
	margin-bottom: 20px;
}
#model-container{
	border: solid 20px #E9ECF1;
	margin-top: 50px;
	background-color: #FCFCFC;
	min-height: 855px;
	min-width: 1400px;
	overflow: hidden;
}
.model-top{
	width: 95%;
	padding: 20px 40px;
}
.con-underline{
	border-bottom: 1px solid #CCCCCC;
	height: 40px;
}
.dns-num{
	border-left: 8px solid #72b16a;
}
.dns-num span{
	padding-left: 15px;
	color: #72b16a;
}
.num-class{
	padding-left:5px!important;
	color: orange!important;
}
</style>
