from fasthtml.common import Script
from pathlib import Path

def read_main():
    with open(f"{Path(__file__).parent}/editor.js", 'r') as f:
        return f.read()

class EditorJS:
    def __init__(self):
        self.script = Script(code=read_main(), type='module')
    def __ft__(self):
        return self.script
 
        
STYLE = f""" .editor {{
 
        margin-top: 2%;
        margin-left: 30%;
        margin-right: 30%;
        
        
        padding: 0;
        font: 18px / 1.375 georgia, serif;
        background: #fff;
        box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.1);
        color: #444;

          padding: 100px 200px;
      }}
            
       .editor.a {{
            color: royalBlue;
            text-decoration: none;
            border-bottom: 1px solid #eee;
        }}

        .editor.h1.ce-header {{
            font-size: 175%;
        }}
        
        .editor.h2.ce-header {{
            text-transform: uppercase;
            margin-top: 2em;
            letter-spacing: 1px;
            font-size: 90%;
        }}
        
        .cdx-list {{
        margin-left: 0;
        padding-left: 0;
        
       /* Save button style */
        .save-button {{
            position: absolute;
            top: 10px;
            right: 500px;
            background-color: transparent;
            border: none;
            cursor: pointer;
        }}

        /* Feather icon styling */
        .feather-icon {{
            width: 14px;
            height: 14px;
      
        }}

        /*  Hover effect */
        .save-button:hover .feather-icon {{ 
            color: #007bff; /* Change color on hover */
        }}
        
        }}"""
        
STYLE = """#content {
     position: relative;
        width: 80%;
        margin: 20px auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 4px;
        min-height: 100px; /* Ensure the content area is visible */
        line-height: 1.5; /* Improve readability */
        white-space: pre-wrap; /* Preserve whitespace formatting */
      }
      .link-wrapper {
        display: inline-block; /* Ensure the wrapper div behaves like an inline element */
      }
      ul,
      ol {
        margin: 0;
        padding-left: 20px;
      }

      img {
        max-width: calc(
          100% - 40px
        ); /* Set the max-width to be slightly less than the container's width */
        height: auto;
        display: block;
        margin: 10px 0; /* Add margin for better spacing */
        
       .placeholder {
            position: absolute;
            top: 10px;
            left: 10px;
            color: #aaa;
            pointer-events: none;
            transition: opacity 0.2s;
        }
        .content-editable:focus + .placeholder,
        .content-editable:not(:empty) + .placeholder {
            opacity: 0;
        }
      }"""