const fs = require("fs");
const ytdl = require("ytdl-core");
const ytsr = require("ytsr");

module.exports = async song => {
  const url = await resolveSongUrl(song);

  const songInfo = await ytdl.getInfo(url).catch(error => {
		switch (error.message) {
			case "Not a youtube domain": return console.error("I can only play songs from Youtube");
			case "Video unavailable": return console.error("the video is unavailable");
			case "This is a private video. Please sign in to verify that you may see it.": return console.error("this video is private");
		};
  });

  console.log(songInfo.videoDetails.lengthSeconds);

  ytdl.downloadFromInfo(songInfo, { filter: "audioonly" }).pipe(fs.createWriteStream("audio.wav"));
};

async function resolveSongUrl(song) {
	if (song.match(/^http/)) return song;

	const result = await ytsr(song, { limit: 1 });

  return result.items[0].url;
}