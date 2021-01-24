<template>
  <div class="home">
    <section class="main-splash">
      <div class="container">
        <div class="row">
          <div class="column">
            <h1>Convert Your Favourite Tunes</h1>
            <br>
          </div>
          <div class="column">
          <img class= "landingImage" alt="Landing Image" src="../assets/landingimage.png" style="float:right"
          </div>
        </div>
      </div>
	  </section>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    HelloWorld
  }
};
</script>
