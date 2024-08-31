from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

# Sample list of items that could be suggested when typing #
sample_items = ["#Python", "#JavaScript", "#HTML", "#CSS", "#FastAPI", "#HTMX"]

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown Editor with HTMX and FastAPI</title>
        <script src="https://unpkg.com/htmx.org@1.9.2"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            #editor {
                width: 600px;
                min-height: 300px;
                border: 1px solid #ccc;
                padding: 10px;
                background-color: #f9f9f9;
                overflow-y: auto;
            }
            #dropdown {
                position: absolute;
                background-color: white;
                border: 1px solid #ccc;
                display: none;
            }
            #dropdown div {
                padding: 5px;
                cursor: pointer;
            }
            #dropdown div:hover {
                background-color: #f0f0f0;
            }
        </style>
    </head>
    <body>
        <h2>Markdown Editor with HTMX and FastAPI</h2>
        <div id="editor" contenteditable="true" hx-trigger="keyup changed delay:500ms" hx-get="/suggest" hx-target="#dropdown" placeholder="Type Markdown here..."></div>
        <div id="dropdown"></div>

        <script>
            document.addEventListener('click', function(event) {
                if (!event.target.closest('#dropdown')) {
                    document.getElementById('dropdown').style.display = 'none';
                }
            });

            function insertTextAtCursor(text) {
                const editor = document.getElementById('editor');
                const selection = window.getSelection();
                if (selection.rangeCount > 0) {
                    const range = selection.getRangeAt(0);
                    range.deleteContents();
                    range.insertNode(document.createTextNode(text));
                    selection.collapseToEnd();
                }
            }

            function showDropdown(items, cursorRect) {
                const dropdown = document.getElementById('dropdown');
                dropdown.innerHTML = '';
                items.forEach(item => {
                    const div = document.createElement('div');
                    div.textContent = item;
                    div.onclick = function() {
                        insertTextAtCursor(item + ' ');
                        dropdown.style.display = 'none';
                    };
                    dropdown.appendChild(div);
                });
                dropdown.style.left = cursorRect.left + 'px';
                dropdown.style.top = cursorRect.bottom + 'px';
                dropdown.style.display = 'block';
            }

            document.getElementById('editor').addEventListener('keyup', function(event) {
                if (event.key === '#') {
                    const range = window.getSelection().getRangeAt(0);
                    const rect = range.getBoundingClientRect();
                    fetch('/suggest').then(response => response.json()).then(data => {
                        showDropdown(data.items, rect);
                    });
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/suggest", response_class=JSONResponse)
async def suggest(request: Request):
    # In a real application, you could filter items based on the current text
    # Here we just return all sample items
    return {"items": sample_items}
