<template>
	<main id="sta-container">
		<div class="main-nav">
      
	       <el-menu default-active="1" class="el-menu-vertical-demo">
           
           <el-submenu index="1">
             <template slot="title"><i class="el-icon-warning"></i>注册信息黑名单 </template> 
             <router-link to='/sta-info/people/people-name'> <el-menu-item index="1-1">注册人姓名黑名单</el-menu-item></router-link>
             <router-link to='/sta-info/people/people-tel'><el-menu-item index="1-2">注册人电话黑名单</el-menu-item></router-link>
             <router-link to='/sta-info/people/people-email'><el-menu-item index="1-3">注册人邮箱黑名单</el-menu-item></router-link>
           </el-submenu>
       
           
						<el-submenu index="2">
			        <template slot="title"><i class="el-icon-menu"></i>域名WHOIS信息展示</template>
			        <router-link to='/sta-info/whois/whois-all'><el-menu-item index="2-1">WHOIS总体概览</el-menu-item></router-link>
			        <router-link to='/sta-info/whois/whois-sign'><el-menu-item index="2-2">非法域名所属注册商</el-menu-item></router-link>
							<router-link to='/sta-info/whois/whois-domains'><el-menu-item index="2-3">非法域名所属顶级域</el-menu-item></router-link>
		        </el-submenu>
           
		      	<router-link to='/sta-info/space/space-info'><el-menu-item index="3"><i class="el-icon-setting"></i>空间维度展示信息</el-menu-item></router-link>
           
		      	<el-submenu index="4">
			        <template slot="title"><i class="el-icon-message"></i>时间维度展示信息</template>
			        <router-link to='/sta-info/time/time-year'><el-menu-item index="4-1">按创建域名/到期域名数量展示</el-menu-item></router-link>
			        <router-link to='/sta-info/time/time-update'><el-menu-item index="4-2">按更新时间频率展示</el-menu-item></router-link>
              <router-link to="/sta-info/time/time-sur"><el-menu-item index="4-3">非法域名总体生存时间</el-menu-item></router-link>
		        </el-submenu>
           
		        <el-submenu index="5">
			        <template slot="title"><i class="el-icon-search"></i>解析DNS和IP的相关信息</template>
			        <router-link to='/sta-info/ip/ip-num'><el-menu-item index="5-1">非法域名的Online/Offline</el-menu-item></router-link>
			        <router-link to='/sta-info/ip/ip-sur'><el-menu-item index="5-2">非法域名IP更换频率图</el-menu-item></router-link>
			        <!--router-link to='/sta-info/ip-fre'><el-menu-item index="6-3">非法域名IP更换频率图</el-menu-item></router-link-->
		        </el-submenu>

            <router-link to='/sta-info/new/new-item'><el-menu-item index="6"><i class="el-icon-setting"></i>新增地图展示</el-menu-item></router-link>
           
		    </el-menu>
    	</div>
    <div class="main-right"> 
      <router-view></router-view>
    </div>


  </main>
</template>




<style>
  #sta-container{
  border: solid 20px #E9ECF1;
  margin-top: 50px;
  background-color: #FCFCFC;
  min-height: 855px;
  min-width: 1400px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  overflow: hidden;
  }
  .main-nav{
  -webkit-box-flex:1;
  -ms-flex:1;
  flex:1;
  background-color: #EEF1F6;

  }
  .main-right{
  -webkit-box-flex:5;
  -ms-flex:5.5;
  flex:5;
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
  /* 路由切换动效 */
  /*.fade-enter-active, .fade-leave-active {
  transition: all .3s;
  }
  .fade-enter, .fade-leave-active {
  opacity: 0;
  }*/
</style>
