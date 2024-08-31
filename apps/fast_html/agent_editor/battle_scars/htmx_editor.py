from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mock data for mentions
mentions_data = {
    "@": ["@alice", "@bob", "@charlie"],
    "#": ["#python", "#fastapi", "#htmx"],
    "/": ["/help", "/about", "/contact"]
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/mentions")
async def get_mentions(command: str=None):
    items = mentions_data.get(command, ['a', 'b', 'c', 'd'])
    return JSONResponse({"items": items}, status_code=200)