<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
h1{
  font-family: Montserrat;
  font-style: normal;
  font-weight: 800;
  font-size: 195px;
  line-height: 238px;
  color: #18181A;
}
h2{
  font-family: Montserrat;
  font-style: normal;
  font-weight: bold;
  font-size: 140px;
  line-height: 171px;
  color: #18181A;
}
h3{
  font-family: Montserrat;
  font-style: normal;
  font-weight: normal;
  font-size: 100px;
  line-height: 122px;
  color: #18181A;
}
h4{
  font-family: Montserrat;
  font-style: normal;
  font-weight: 800;
  font-size: 40px;
  line-height: 49px;
  color: #727272;
}


</style>
