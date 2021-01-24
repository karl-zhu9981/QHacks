let http = require("http");
const getSong = require("./src/getSong.js");
const midiToPdf = require("./src/midiToPdf.js");
const spawn = require("child_process").spawn;

http.createServer((request, response) => {
  response.writeHead(200, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  });

  let chunks = [];

  request.on("data", chunk => chunks.push(chunk));
  request.on("end", async () => {
    const responseBody = Buffer.concat(chunks).toString();
    chunks = null;
    await getSong(responseBody).catch(error => {
      console.log(error)
    });
    const pythonProcess = spawn("python", ["../../main.py"]);
    pythonProcess.stdout.on("data", data => {
      // do something
    });
  });
}).listen(8000);

http = null;
delete require.cache[require.resolve("http")];

console.log("Server running on port 8000");