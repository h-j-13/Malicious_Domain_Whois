<template>
  <div id="app">
    <head1></head1> 
    <router-view></router-view>
  </div>
</template>

<script>
import Vue from 'vue'
import head1 from './components/header.vue'

export default {
  name: 'app',
  components: {head1},
  data () {
    return{
      Atest:'hello world',
      activeIndex: '1'
    }
  },
  methods: {
      
    }
}
</script>

<style>
html,body{
  margin: 0;
  padding: 0;
  height: 95%;
}
a{
  text-decoration: none;
  outline: none;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
}
</style>
