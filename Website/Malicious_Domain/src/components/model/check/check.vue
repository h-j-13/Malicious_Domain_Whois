<template>
	<main>
		<el-row>
			<el-col :span="24">
		<div id="model-container">
			<div class="model-top">
				<div id="leftpart">
					<checktype></checktype>
					<div id="lenline"></div>
					<checkwhois></checkwhois>
					<div id="lenline"></div>
					<checkip></checkip>
					<div id="lenline"></div>
					<checkphoto></checkphoto>
					<div id="lenline"></div>
					<checkspace></checkspace>
				</div>
				<div id="illline"></div>
				<div id="rightpart">
					<checkreson></checkreson>
					<div id="lenline"></div>
					<checkpower></checkpower>
					<div id="lenline"></div>
					<checksame></checksame>
				</div>
			</div>
		</div>
	</el-col>
		</el-row>
	</main>
</template>

<script>
import checktype from "./check-type.vue"
import checkspace from "./check-space.vue"
import checkwhois from "./check-whois.vue"
import checkip from "./check-ip.vue"
import checkphoto from "./check-photo.vue"
import checkreson from "./check-reson.vue"
import checkpower from "./check-power.vue"
import checksame from "./check-same.vue"
	export default{
		data(){
			return{
			}
		},
		/*methods: {
      onSubmit() {
        alert('SECUSS');
      }
    },*/
		components:{checktype,checkwhois,checkip,checkphoto,checkspace,checkreson,checkpower,checksame},
	}
</script>

<style>
#checktype{
	margin-top: 10px;
  margin-left: 10px;
}
#checkwhois{
	margin-top: 10px;
  margin-left: 10px;
	width:80%;
}
#checkip{
	margin-top: 10px;
  margin-left: 10px;
	width:80%;
}
#checkphoto{
	margin-top: 10px;
  margin-left: 10px;
	width:40%;
}
#checkspace{
	margin-top: 10px;
  margin-left: 10px;
	width:40%;
}
#checkspace{
		margin-top: 10px;
		margin-left: 10px;
		width: 40%;
		height: 50%;
}
#checkreson{
		margin-top: 10px;
		margin-left: 10px;
		width: 40%;
		height: 60%;
}
#checkpower{
		margin-top: 10px;
		margin-left: 10px;
		width: 80%;
		height: 60%;
}
#checksame{
		margin-top: 10px;
		margin-left: 10px;
		width: 40%;
		height: 60%;
}
#lenline{
	width: 80%;
	height: 20px;
	margin-left: 10px;
	margin-top: 0px;
	margin-bottom: 20px;
	border-bottom: 1px solid #cccccc;
}
#leftpart{
	width: 47%;
	margin-left: 40px;
	float: left;
}
#illline{
	height: 1900px;
	margin-right: 20px;
	width: 1px;
	border-left: 1px solid #cccccc;
	float: left;
}
#rightpart{
	width: 47%;
	margin-left: 40px;
	float: left;
}
</style>
