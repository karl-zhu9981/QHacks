const fs = require("fs");
const ytdl = require("ytdl-core");
const ytsr = require("ytsr");

module.exports = searchString => {
  return new Promise(async (resolve, reject) => {
    const url = await resolveSongUrl(searchString);

    const songInfo = await ytdl.getInfo(url).catch(error => {
      switch (error.message) {
        case "Not a youtube domain": return console.error("I can only play songs from Youtube");
        case "Video unavailable": return console.error("the video is unavailable");
        case "This is a private video. Please sign in to verify that you may see it.": return console.error("this video is private");
      };
    });
    const timeStamp = new Date().getTime();
    const file = fs.createWriteStream(`./downloads/${ timeStamp }.wav`);
    ytdl.downloadFromInfo(songInfo, { filter: "audioonly" }).pipe(file);

    file.on("finish", () => resolve(timeStamp));
  });
};

async function resolveSongUrl(searchString) {
	if (searchString.match(/^http/)) return searchString;

	const result = await ytsr(searchString, { limit: 1 });

  return result.items[0].url;
}