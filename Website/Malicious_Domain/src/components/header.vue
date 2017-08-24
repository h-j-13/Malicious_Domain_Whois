<template>
	<header>
	<el-row>
		<el-col :span="24">
		<el-menu :default-active="activeIndex" :active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" router>
			<el-menu-item index='/'>首页</el-menu-item>
			<el-menu-item index='/sta-info/people/people-name'>非法域名统计信息</el-menu-item>
			<el-menu-item index='/model'>域名评估</el-menu-item>
			<el-menu-item index='/check' v-if="success">域名画像评估报告</el-menu-item>
		</el-menu>
		</el-col>
	</el-row>
	</header>
</template>

<script>
import sub from "./model/model.vue"
  export default {
    data() {
      return {
        activeIndex: '/',
        success:sub,
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        
      },
      get_index(){
      	this.activeIndex = this.$store.state.index;
      }
    },
    watch:{
    	'$store.state.index':'get_index'
    }
  }
</script>

<style>
header{
	box-shadow: 0 2px 4px 0 rgba(0,0,0,.12),0 0 6px 0 rgba(0,0,0,.04);
	position: fixed;
	top: 0;left: 0;right: 0;
	z-index: 1000;
}
header .el-menu-demo{
	padding-left: 1%;
}
</style>
