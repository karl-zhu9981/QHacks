const fs = require("fs");
let http = require("http");
const getSong = require("./src/getSong.js");
const midiToPdf = require("./src/midiToPdf.js");
const wavToMidiUrl = require("./src/wavToMidiUrl.js");
const downloadMidi = require("./src/downloadMidi.js");

http.createServer((request, response) => {
  response.writeHead(200, {
    "Content-Type": "application/pdf",
    "Access-Control-Allow-Origin": "*"
  });

  let chunks = [];

  request.on("data", chunk => chunks.push(chunk));
  request.on("end", async () => {
    const responseBody = Buffer.concat(chunks).toString();
    chunks = null;
    const timestamp = await getSong(responseBody).catch(error => console.log(error));
    const midiUrl = await wavToMidiUrl(timestamp);
    await downloadMidi(midiUrl, timestamp);
    await midiToPdf(timestamp);
    const file = fs.readFileSync(`./${ timestamp }.pdf`);
    response.write(file);
    response.end();
  });
}).listen(8000);

http = null;
delete require.cache[require.resolve("http")];

console.log("Server running on port 8000");