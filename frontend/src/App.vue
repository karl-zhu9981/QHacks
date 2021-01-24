<template>
  <div id="app">
    <link rel='stylesheet' id='google-fonts-1-css'  href='https://fonts.googleapis.com/css?family=Montserrat%3A100%2C100italic%2C200%2C200italic%2C300%2C300italic%2C400%2C400italic%2C500%2C500italic%2C600%2C600italic%2C700%2C700italic%2C800%2C800italic%2C900%2C900italic&#038;ver=5.5.3' type='text/css' media='all' />
    <div id="nav">
      <img class= "logo" alt="Youtune" src="@/assets/Youtune.png" width='2%'>
      <router-link to="/">Home </router-link>
      <router-link to="/about">About </router-link>
    </div>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: Montserrat;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: hsl(0, 0%, 100%);
  padding: 60px;
}
#nav {
  padding: 20px;
  padding-bottom: 70px;
  text-align: right;
  a {
    font-weight: bold;
    color: #686767;
    text-decoration: none;
    &.router-link-exact-active {
      color: #18181A;
      text-decoration: none;
    }
  }
}
input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 80px;
  box-sizing: border-box;
  border: 4px solid #A397EF;
  box-sizing: border-box;
}
.container{
  display:flex;
  align-items: center
}
.logo{ 
	position:fixed; 
	left:60px; 
  max-width: 20%;
} 
.landingImage{
  max-width: 80%;
  float: right;
}
.row::after {
  content: "";
  clear: both;
  display: table;
}
h1{
  font-family: Montserrat;
  font-style: normal;
  font-weight: 900;
  font-size: 5.5rem;
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
  text-decoration: none;
  color: #727272;
}


</style>
