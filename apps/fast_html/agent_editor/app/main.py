from fasthtml.common import *
from modules import EditorJS
from modules.editor import STYLE
from models.AgentSpec import AgentSpec
import json
from starlette.responses import JSONResponse

from pathlib import Path

def read_main():
    with open(f"{Path(__file__).parent}/modules/editor/simple_editor.js", 'r') as f:
        return f.read()
 
styles = Style(STYLE)
feather_icons = Script(src='https://unpkg.com/feather-icons')
hdrs = [ styles, feather_icons,  Script(code=read_main())]#,  EditorJS()
app,rt = fast_app(live=True, hdrs=hdrs,pico=False)

@rt('/json')
def get():
    return JSONResponse(AgentSpec.load_agents(), status_code=200, )

@rt('/')
def get(value:str=None):
    print(value)
    #return Div(*AgentSpec.load_agents())
    return Div( *[Div(id="content",
                    contenteditable="true",
                    hx_trigger="keyup[['#'].includes(event.key) ]",
                    hx_vals=f"js:{{key: event.key, cursorPosition: replaceSymbolWithSpan(event, document.getElementById('content'))}}",
                    hx_target="#options",
                    hx_swap='outerHTML',
                    hx_post="/ask" ),
                 Div(id='options', 
                     hx_swap_oob=True,
                     style="position: absolute; display: none; border: 1px solid black; background-color: white; padding: 5px; width: 150px; top: 10px; left: 52px"),
                 #Div('Type @, #, or / to see options...', cls="placeholder"),
                 Script(code="""me().addEventListener("paste", handlePaste); me().addEventListener("keydown", keydown_handler);""")],
               style='position: relative',
              
               )
#hx-focus="#content"


@app.get('/span')
def span(value:str):
    """the minus 54 thing is a #<br> hack im trying to figure out"""
    print(value, 'is the value')
    return  value

@app.post('/ask')
def ask_for(data:dict):
    print(data)
    key = data.get('key')
    data = json.loads(data.get('cursorPosition'))
    tid = data.get('tid')
    
    content = data.get('content')
    x = 10
    y = 10

    pattern = r'id="([^"]+)"'
    matches = re.findall(pattern, content.replace("/",""))
  
    style = f"position: absolute; display: block; border: 1px solid black; background-color: white; padding: 5px; width: 150px; top: {int(y)+15}px; left: {int(x)}px"
    print(style)
    """ask for a span to place into the end of test - but actually we will want a smarter insertion method"""
    selections = [Div(s,
                      hx_get=f"/span", 
                      hx_trigger="click",
                      hx_vals={'value': s},
                      hx_target=f"#{matches[0]}", 
                      hx_swap="outerHTML",
                      style="cursor: pointer",
                      onclick=f"document.getElementById('options').style.display='none';"
                      ) for i, s in enumerate(['Option 1', 'Option 2', 'Option 3', 'Option 4'])]
    
    return Div(*selections, id='options', style=style,   )

@app.get('/edit')
def get(): return Div(Div( cls='editor', id='editorjs'),
                      Script(code='feather.replace()')  )

@app.post('/save')
def post_data(data:dict):
    print(data)
    data = data.get('blocks')
    if data:
        a = AgentSpec.parse_agent_data(data)
        """HACK to make sure the change is legit - depends on init text!!
        - obviously we just need more buttons to do this properly"""
        if a.description != 'Your agent description':
            a.save()
    return Response(status_code=201)

@app.get('/preview_link')
def get_stuff(url:str=None):
    f = utils.describe_openapi_json_as_function(endpoint=url)
    url = json.loads(f.metadata).get('url')
    image_url = None
    return {
    "success" : 1,
    "link": url, 
    "meta": {
        "title" : f.name,
        "description" : f.description,
        "image" : {
            "url" : image_url
        }
    }
}
    
@app.get('/refs')
def get_stuff(search:str=None):

    return {
        "success": True,
        "items": [
            {
            "href": "http://www.google.com",
            "name": "The first item",
            "description": ""
            },
            {
            "href": "https://codex.so/media",
            "name": "The second item",
            "description": ""
            }
        ]
        }

serve(port=4001)