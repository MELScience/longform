// a simple TeX-input example
var mjAPI = require("mathjax-node/lib/mj-single.js");
mjAPI.config({
  MathJax: {
      // traditional MathJax configuration
  }
});
mjAPI.start();

var yourMath = process.argv[2];

mjAPI.typeset({
  math: yourMath,
  format: "TeX", // "inline-TeX", "MathML"
  svg:true
}, function (data) {
  if (!data.errors) {console.log(data.svg)}
});
