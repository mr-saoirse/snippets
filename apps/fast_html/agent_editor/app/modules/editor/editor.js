import EditorJS from "https://cdn.skypack.dev/@editorjs/editorjs";
import Header from "https://cdn.skypack.dev/@editorjs/header";
import LinkAutocomplete from "https://cdn.skypack.dev/@editorjs/link-autocomplete";
import Table from "https://cdn.skypack.dev/@editorjs/table";
import Paragraph from "https://cdn.skypack.dev/@editorjs/paragraph";
import LinkTool from "https://cdn.skypack.dev/@editorjs/link";


const message = greet('World');
console.log(message);

function debounce(func, delay) {
  let timer;
  return function () {
    const context = this;
    const args = arguments;
    clearTimeout(timer);
    timer = setTimeout(() => func.apply(context, args), delay);
  };
}

async function save_content(content) {
  const sanitizedData = JSON.stringify(content);
  const response = await fetch('/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      //'CSRF-Token': csrfToken  // Include CSRF token in request headers
    },
    body: sanitizedData
  });

  if (!response.ok) {
    throw new Error('Failed to save content');
  }

  const result = await response;
  //TODO properly handle response
  console.log('Content saved successfully:', result);
}

const debounce_save_content = debounce(save_content, 2000)

function initializeEditor() {
  //loadEditorStyles();
  const editor = new EditorJS({
    holder: 'editorjs',
    tools: {
      header: Header,
      //mention: Mention,
      table: {
        class: Table,
        inlineToolbar: true,
      },
      linkTool: {
        class: LinkTool,
        config: {
          endpoint: "/preview_link",
        },
      },
      paragraph: {
        class: Paragraph,
        inlineToolbar: true,
      },
      link: {
        class: LinkAutocomplete,
        config: {
          endpoint: "/refs",
          queryParam: "search",
        },
      },
    },
    placeholder: 'Fill in any details about your agent (name, description, types and functions)', // Placeholder text for the Editor.js container
    autofocus: true, // Autofocus on the editor when the page loads
    data: {
      blocks: [
        {
          type: 'header',
          data: {
            text: 'Your agent name',
            level: 1
          }
        },
        {
          type: 'paragraph',
          data: {
            text: 'Your agent description'
          }
        },
        {
          type: 'header',
          data: {
            text: 'Structured Responses (Optional)',
            level: 2
          }
        },
        {
          type: 'header',
          data: {
            text: 'TypeA',
            level: 3
          }
        },
        {
          type: 'table',
          data: {
            content: [
              ['<b>Field</b>', '<b>Description</b>', '<b>Type</b>'],
            ]
          }
        },
        {
          type: 'header',
          data: {
            text: 'Links to functions (API Endpoints)',
            level: 2
          }
        },
      ]
    },

    onChange: (api, event) => {
      console.log('Now I know that Editor\'s content changed!', event)

      editor.save().then((outputData) => {
        console.log(outputData)
        debounce_save_content(outputData)

      });
    }

  });




  return editor;
}

initializeEditor();
