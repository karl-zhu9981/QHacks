const getSong = require("./getSong.js");
const http = require("http");

http.createServer((request, response) => {
  response.writeHead(200, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  });

  let chunks = [];

  request.on("data", chunk => chunks.push(chunk));
  request.on("end", () => {
    const responseBody = Buffer.concat(chunks).toString();
    chunks = null;
    getSong(responseBody);
  });
}).listen(8000);
console.log("Server running on port 8000");