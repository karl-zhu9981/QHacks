<template>
  <div id="app">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <div id="nav">
      <router-link to="/">Home </router-link> |
      <router-link to="/about">About </router-link>
    </div>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: hsl(0, 0%, 100%);
}
#nav {
  padding: 30px;
  text-align: right;
  a {
    font-weight: bold;
    color: #686767;
    &.router-link-exact-active {
      color: #18181A;
    }
  }
}
.landingImage{
	max-width: 50%;
  float: right;
}
}
.row::after {
  content: "";
  clear: both;
  display: table;
}
h1{
  font-family: Avenir;
  font-style: normal;
  font-weight: 800;
  font-size: 3.5rem;
  color: #18181A;
}
h2{
  font-family: Montserrat;
  font-style: normal;
  font-weight: bold;
  color: #18181A;
}
h3{
  font-family: Montserrat;
  font-style: normal;
  font-weight: normal;
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
