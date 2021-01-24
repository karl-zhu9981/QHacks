<template>
  <div class="convert">
    <input v-model="searchString" type="text" placeholder="Paste a Youtube Url..." />
    <button @click="downloadSong(searchString)">Convert</button>
    <div v-if="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import http from "http";

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