"""
this minimal version just focuses on the single page experience
we should follow up with other chat experiences but this shows the core idea
"""

from fasthtml.common import *
import urllib.parse
from pathlib import Path

"""read the script from file -  this is a bad practice if the JS is not reloaded on fast reload!!
"""
with open(f"{Path(__file__).parent}/scripts/module.js", 'r') as f:
    script = f.read()
    
"""some styles"""
# INPUT_STYLE = 'pl-4 p-2 rounded-l-full border border-gray-300 focus:outline-none w-200 font-serif text-stone-600 font-medium'
# BUTTON_STYLE = 'p-2 bg-stone-400 text-white  ml-2 border border-stone-100 hover:border hover:border-stone-300'
# tailwind = Script(src="https://cdn.tailwindcss.com")
#bootstrap_icons = Link(rel='stylesheet', href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css")
"""we need both the style and script for highlighter"""
highlighter = [Link(rel='stylesheet', href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css"), 
               Script(src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js')]
sse = Script(src='https://unpkg.com/htmx-ext-sse@2.2.2/sse.js')#V2!
hdrs = [sse,   *highlighter,  Script(code=script, type='module')]

"""disable pico or it screws with what we are doing with tailwind"""
app, rt = fast_app(hdrs=hdrs, live=True, pico=False, debug=True)

def sse_stream_components(question):
    """Simple control that is ready to ask
    #thanks do this stack overflow question as i would have been lost!
    https://stackoverflow.com/questions/77387165/how-to-politely-close-an-sse-event-stream-using-htmx
    """
    sse = Div(
        Div(*[
            question,
            #this contains both the stream subscription and the swap out on completion
            #BE SURE to use OuterHTML because inner would subtly hid the div but kept the subscription open
            #you should confirm closed and node replace event in the console logs
            Div(sse_swap='message', hx_target='#canvas', hx_swap='beforeend'),
            Div(sse_swap='completed', hx_target='#sse', hx_swap='outerHTML' )],
            hx_ext='sse', 
            id="sse",
            #this is temp to protect using tokens by mistake
            sse_connect=f'http://localhost:5009/ask?question={urllib.parse.quote(question)}' if question else ""  ))

    """return both the sse control and the canvas to write into"""
    #, cls='font-serif text-stone-600 font-medium' 
    return sse, Div(  id='canvas', cls='marked' )


@rt("/", methods=['get','post'])
async def home(question:str=None, data:str=None):
    """"""
    print(question)
    canvas = Div(*sse_stream_components(question), cls='p-5')
     
    """some controls for taking in an input question"""
    button = Button('Go', )
    input =  Input(id='question', style='width: 500px', placeholder='Ask a question about FastHTML...')
    form = Form(Group(input, button), hx_post='/')
    
    input_group = Div(*[form, canvas], cls='w-full absolute top-1/3' )
    
    """composition of controls with a centering style"""
    return   Div(*[ input_group], cls='relative flex justify-center max-w-xl flex-col mx-auto items-center h-screen') 


serve(port=5008)



