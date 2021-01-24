const fs = require("fs");
const axios = require("axios");

module.exports = (url, id) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "get",
      url,
      responseType: "stream"
    }).then(response => {
      const file = fs.createWriteStream(`./downloads/${ id }.midi`);
      response.data.pipe(file);
      file.on("finish", resolve);
    });
  });
}