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
                  <input id="youtubesite" v-model="searchString" type="text" name="youtubesite" placeholder="Paste a Youtube URL Link..."><br>
                  <div id="convert" @click="downloadSong(searchString)"><h4>Convert</h4></div>
                </div>
            </form>
            <br>
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
import http from "http";

export default {
  name: "Home",
  data() {
    return {
      searchString: "",
      errorMessage: "",
      error: false
    }
  },
  methods: {
    async downloadSong(searchString) {
      const client = http.request({
        hostname : "localhost",
        port : 8000,
        method : "POST",
        path : "/"
      }, response => {
        let chunks = [];

				response.on("data", chunk => chunks.push(chunk));
				response.on("end", () => {
					const responseBody = Buffer.concat(chunks).toString();
					chunks = null;
				});
      });
      client.write(searchString);
      client.end();
    }
  }
};
</script>

<style scoped>
div#convert {
  background: #6E67A9;
  border-radius: 84px;
	padding: 0% 14% ;
	text-align: center;
	text-decoration: none;
	font-weight: 700;
	cursor: pointer;
  display: inline-block;
  float: right;
  margin: -78px;
  position: relative;
}
</style>