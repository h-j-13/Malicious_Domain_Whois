<template>
	<div id="home-container">
		<canvas id="home-canvas" width="1419" height="264"></canvas>
		<div class="home-contant">
			<div class="home-show">
				<h1>非法域名挖掘与画像系统</h1>
				<p>评估域名性质，画像立体描述，挖掘非法域名，提供管控线索，展示整体趋势，让非法域名尽在掌控</p>
				<router-link to='/model'><button class="home-button">域名评估</button></router-link>
				<div></div>
				<div class="show-fun" :class="[isPoint?'el-icon-arrow-down':'el-icon-arrow-up']" @click="showClick">
				</div>
				<transition name="mainTran">
					<div class="home-main" v-show="!isPoint">
						<router-link to='/sta-info/people/people-name'><button @click="change()" class="h-button">非法注册人黑名单</button></router-link>
						<router-link to='sta-info/whois/whois-all'><button @click="change()" class="h-button">域名WHOIS信息展示</button></router-link>
						<router-link to='/sta-info/space/space-info'><button @click="change()" class="h-button">空间维度信息展示</button></router-link>
						<router-link to='/sta-info/time/time-year'><button @click="change()" class="h-button">时间维度信息展示</button></router-link>
						<router-link to='/sta-info/ip/ip-num'><button @click="change()" class="h-button">DNS和IP相关信息</button></router-link>
					</div>
				</transition>
			</div>
		</div>
	</div>
</template>

<script>
	export default{
		data () {
			return{
				isPoint:true
			}
		},
		mounted() {
		 	  var canvas = document.getElementById("home-canvas");
			  var ctx = canvas.getContext("2d");
			  var cw = canvas.width = window.innerWidth,
			    cx = cw / 2;
			  var ch = canvas.height = window.innerHeight,
			    cy = ch / 2;

			  ctx.fillStyle = "#000";
			  var linesNum = 16;
			  var linesRy = [];
			  var requestId = null;

			  function Line(flag) {
			    this.flag = flag;
			    this.a = {};
			    this.b = {};
			    if (flag == "v") {
			      this.a.y = 0;
			      this.b.y = ch;
			      this.a.x = randomIntFromInterval(0, ch);
			      this.b.x = randomIntFromInterval(0, ch);
			    } else if (flag == "h") {
			      this.a.x = 0;
			      this.b.x = cw;
			      this.a.y = randomIntFromInterval(0, cw);
			      this.b.y = randomIntFromInterval(0, cw);
			    }
			    this.va = randomIntFromInterval(25, 100) / 100;
			    this.vb = randomIntFromInterval(25, 100) / 100;

			    this.draw = function() {
			      ctx.strokeStyle = "#ccc";
			      ctx.beginPath();
			      ctx.moveTo(this.a.x, this.a.y);
			      ctx.lineTo(this.b.x, this.b.y);
			      ctx.stroke();
			    }

			    this.update = function() {
			      if (this.flag == "v") {
			        this.a.x += this.va;
			        this.b.x += this.vb;
			      } else if (flag == "h") {
			        this.a.y += this.va;
			        this.b.y += this.vb;
			      }

			      this.edges();
			    }

			    this.edges = function() {
			      if (this.flag == "v") {
			        if (this.a.x < 0 || this.a.x > cw) {
			          this.va *= -1;
			        }
			        if (this.b.x < 0 || this.b.x > cw) {
			          this.vb *= -1;
			        }
			      } else if (flag == "h") {
			        if (this.a.y < 0 || this.a.y > ch) {
			          this.va *= -1;
			        }
			        if (this.b.y < 0 || this.b.y > ch) {
			          this.vb *= -1;
			        }
			      }
			    }

			  }

			  for (var i = 0; i < linesNum; i++) {
			    var flag = i % 2 == 0 ? "h" : "v";
			    var l = new Line(flag);
			    linesRy.push(l);
			  }

			  function Draw() {
			    requestId = window.requestAnimationFrame(Draw);
			    ctx.clearRect(0, 0, cw, ch);

			    for (var i = 0; i < linesRy.length; i++) {
			      var l = linesRy[i];
			      l.draw();
			      l.update();
			    }
			    for (var i = 0; i < linesRy.length; i++) {
			      var l = linesRy[i];
			      for (var j = i + 1; j < linesRy.length; j++) {
			        var l1 = linesRy[j]
			        Intersect2lines(l, l1);
			      }
			    }
			  }

			  function Init() {
			    linesRy.length = 0;
			    for (var i = 0; i < linesNum; i++) {
			      var flag = i % 2 == 0 ? "h" : "v";
			      var l = new Line(flag);
			      linesRy.push(l);
			    }

			    if (requestId) {
			      window.cancelAnimationFrame(requestId);
			      requestId = null;
			    }

			    cw = canvas.width = window.innerWidth,
			      cx = cw / 2;
			    ch = canvas.height = window.innerHeight,
			      cy = ch / 2;

			    Draw();
			  };

			  setTimeout(function() {
			    Init();

			    addEventListener('resize', Init, false);
			  }, 15);

			  function Intersect2lines(l1, l2) {
			    var p1 = l1.a,
			      p2 = l1.b,
			      p3 = l2.a,
			      p4 = l2.b;
			    var denominator = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y);
			    var ua = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) / denominator;
			    var ub = ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) / denominator;
			    var x = p1.x + ua * (p2.x - p1.x);
			    var y = p1.y + ua * (p2.y - p1.y);
			    if (ua > 0 && ub > 0) {
			      markPoint({
			        x: x,
			        y: y
			      })
			    }
			  }

			  function markPoint(p) {
			    ctx.beginPath();
			    ctx.arc(p.x, p.y, 2, 0, 2 * Math.PI);
			    ctx.fill();
			  }

			  function randomIntFromInterval(mn, mx) {
			    return ~~(Math.random() * (mx - mn + 1) + mn);
			  }
    	 },
    	methods:{
    	 	showClick:function(e){
    	 		this.isPoint = !this.isPoint
    	 	},
    	 	change:function(){
    	 		
    	 	}
    	 }
	}
</script>

<style>
	#home-container{
		background-color: #F8F8F8;
	  	overflow: hidden;
	  	position: relative;
	}
	#home-canvas{
		background-color: #F8F8F8;
		z-index: -1000;
	}
	.home-contant{
		z-index:1;
		position: absolute;
		width: 100%;
		left: -20px;
		top: 200px;
	}
	.home-show{
		text-align:center;
		font-family: "微软雅黑";
	}
	.home-show h1{
		font-size: 42px;
	}
	.home-show p{
		font-size: 18px;
	}
	.home-button{
	    background-color: #08A9F2; /* Green */
    	border: 2px solid #08A9F2;
	    color: white;
	    height: 50px;
	    padding: 7px 32px;
	    text-align: center;
	    text-decoration: none;
	    display: inline-block;
	    font-size: 20px;
	    margin: 12px 2px;
	    -webkit-transition-duration: 0.4s; /* Safari */
	    transition-duration: 0.4s;
	    cursor: pointer;
	    color: white;
	}
	.home-button:hover{
	    background-color: white; 
   		color: black; 
	}
	.show-fun{
		margin-top:30px;
	}
	.show-fun:hover{
		cursor: pointer; 
		color: #ADD8E6;
	}
	.mainTran-enter-active, .mainTran-leave-active {
	  transition: opacity .7s
	}
	.mainTran-enter, .mainTran-leave-active {
	  opacity: 0
	}
	.home-main{
		margin-top: 40px;
	}
	.h-button{
	    border: 1px solid #ADD8E6;
	    color: white;
	    height: 45px;
	    padding: 5px 32px;
	    text-align: center;
	    text-decoration: none;
	    display: inline-block;
	    font-size: 16px;
	    margin: 4px 2px;
	    -webkit-transition-duration: 0.4s; /* Safari */
	    transition-duration: 0.4s;
	    cursor: pointer;
		background-color: white; 
   		color: black; 
	}
	.h-button:hover{
		background-color: orange; 
   		color: white; 
	}
</style>