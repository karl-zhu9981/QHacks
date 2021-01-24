<template>
  <div class="home">
    <section class="main-splash">
      <div class="container">
          <div class="text-col">
            <h1>Convert Your Favourite Tunes</h1>
            <br>
            <form>
                <label for="fname"></label><br>
                <div class="buttonwrapper">
                  <input type="text" id="youtubesite" name="youtubesite" placeholder="Paste a Youtube URL Link..."><br>
                  <router-link to="{ name: 'Convert' }" tag="li"><h4>Convert</h4></router-link>
                </div>
            </form>
            <br>
            <br>
          </div>
          <div class="image-col">
            <br>
            <img class= "landingImage" alt="Landing Image" src="../assets/landingimage.png">
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
