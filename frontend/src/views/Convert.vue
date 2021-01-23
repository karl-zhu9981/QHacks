<template>
  <div class="about">
    <input v-model="searchString" type="text" placeholder="Paste a Youtube Url..." />
    <button @click="downloadSong(searchString)">Convert</button>
    <div v-if="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Convert",
  data() {
    return {
      searchString: "",
      errorMessage: "",
      error: false
    }
  },
  methods: {
    async downloadSong(searchString) {
      // make a post request to our backend
    }
  }
};
</script>