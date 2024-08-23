//
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

let all_content = ''
const markdownDiv = document.getElementById("canvas");

//SETUP MARKDOWN assume highlight imported
marked.setOptions({
    highlight: function (code, lang) {
        return hljs.highlightAuto(code, [lang]).value;
    }
});

//we are always watching all content
function updateMarkdown() {
    console.log('updating markdown')
    markdownDiv.innerHTML = marked(all_content);
}

document.addEventListener('htmx:afterSwap', function(event) {
      console.log('swapping')
      //console.log(event.target) 
});

document.addEventListener('htmx:sseBeforeMessage', function (e) {
  //console.log('****receiving***');
  //console.log(e.detail);
  console.log(e.detail)
  let decoded_data = atob(e.detail.data)
  all_content += decoded_data;
  console.log(all_content);
  //prevent setting since we clocked and decoded
  //the completed swap needs to happen to kill the div
  if (e.detail.type != 'completed')
    e.preventDefault();
  //update the markdown using all content consumed
  updateMarkdown();
});

//for debugging
document.addEventListener('htmx:sseClose', function (e) {
    console.log('close');
    const reason = e.detail.type
    switch(reason) {
        case "nodeMissing":
            console.log(reason);
        case "nodeReplaced":
            console.log(reason);
            //this is the simplest way to make the markdown render replace on next call for this minimal version
            all_content = ''
        case "message":
            console.log(reason);
    }
}); 