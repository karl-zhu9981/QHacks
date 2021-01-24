const midiToPdf = require("./src/midiToPdf.js");

midiToPdf("audio");
// const getSong = require("./getSong.js");
// let http = require("http");
//
// http.createServer((request, response) => {
//   response.writeHead(200, {
//     "Content-Type": "application/json",
//     "Access-Control-Allow-Origin": "*"
//   });
//
//   let chunks = [];
//
//   request.on("data", chunk => chunks.push(chunk));
//   request.on("end", async () => {
//     const responseBody = Buffer.concat(chunks).toString();
//     chunks = null;
//     const buffer = await getSong(responseBody);
//     // console.log(buffer)
//   });
// }).listen(8000);
//
// http = null;
// delete require.cache[require.resolve("http")];
//
// console.log("Server running on port 8000");