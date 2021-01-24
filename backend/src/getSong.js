const fs = require("fs");
const ytdl = require("ytdl-core");
const ytsr = require("ytsr");

module.exports = searchString => {
  return new Promise(async (resolve, reject) => {
    const url = await resolveSongUrl(searchString);

    const songInfo = await ytdl.getInfo(url).catch(error => {
      switch (error.message) {
        case "Not a youtube domain": reject("I can only play songs from Youtube");
        case "Video unavailable": reject("the video is unavailable");
        case "This is a private video. Please sign in to verify that you may see it.": reject("this video is private");
      };
    });
    const timestamp = new Date().getTime();
    const file = fs.createWriteStream(`../midiconversion/${ "default" }.wav`);
    ytdl.downloadFromInfo(songInfo, { filter: "audioonly" }).pipe(file);

    file.on("finish", () => resolve(timestamp));
  });
};

async function resolveSongUrl(searchString) {
	if (searchString.match(/^http/)) return searchString;

	const result = await ytsr(searchString, { limit: 1 });

  return result.items[0].url;
}