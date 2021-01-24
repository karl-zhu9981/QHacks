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
import axios from "axios";

export default {
  name: "Home",
  data() {
    return {
      searchString: ""
    }
  },
  methods: {
    async downloadSong(searchString) {
      if (!searchString) return;
      axios.post("http://localhost:8000", searchString, {
        responseType: "arraybuffer"
      }).then(response => this.saveByteArray(response.data));
    },
    saveByteArray(responseBody) {
      const url = window.URL.createObjectURL(new Blob([responseBody], {
        type: "arraybuffer"
      }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "sheet.pdf");
      document.body.appendChild(link);
      link.click();
    }
  }
};
</script>

<style scoped>
div#convert {
  background: #6E67A9;
  border-radius: 84px;
	padding: 0% 14%;
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