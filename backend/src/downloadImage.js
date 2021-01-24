const fs = require("fs");
const axios = require("axios");

module.exports = (url, page) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "get",
      url,
      responseType: "stream"
    }).then(response => {
      const file = fs.createWriteStream(`./pages/${ page }.jpg`);
      response.data.pipe(file);
      file.on("finish", resolve);
    }).catch(error => {
      if (!error) return;
      if (!error.response) console.log(error);
      switch (error.response.status) {
        case 503: resolve(this.exec(url)); break;
      }
    });
  });
}