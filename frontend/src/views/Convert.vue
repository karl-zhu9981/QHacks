<template>
  <div class="convert">
    <input v-model="searchString" type="text" placeholder="Paste a Youtube Url..." />
    <button @click="downloadSong(searchString)">Convert</button>
    <div v-if="error">{{ errorMessage }}</div>
  </div>
</template>