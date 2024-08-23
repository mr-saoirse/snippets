"""
the server handles Q&A and also a dummy streaming endpoint
"""

from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from fastapi.exceptions import  HTTPException
import time
import base64

def b64encode(s):
    base64_bytes = base64.b64encode(s.encode('utf-8'))
    return   base64_bytes.decode('utf-8')

#the origin MUST match the origin in the request - i struggled with this trying localhost for example
#null is added for some simple html page examples that have no origin in the request
origins = ['http://0.0.0.0:5008', 'http://localhost:5009', 'http://0.0.0.0:5009', 'null']
app = FastAPI()
app.add_middleware( CORSMiddleware,
        allow_origins=origins,
        #this allow credentials must be true unless there is a way to disable auth in events
        #which i dont know how to do: SSE uses event sources 
        #https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'])

def buffer_term(s):
    return  f"""event: completed
data: \n\n"""

@app.get('/dummy') 
def dummy_stream():
    def stream():
        """
        ive set this to maxout at 300 just to get some samples
        """
        buffer = []
        for idx in range(100):
            """create a dummy span"""
            msg = f"<span>This is {idx} </span>"
            """concatenate it"""
            buffer.append(str(msg))
            """create the event stream format"""
            msg = f"data: {msg} \n\n"
            yield msg
            time.sleep(.025)
        yield buffer_term("".join(buffer))

    return StreamingResponse(stream(),  media_type='text/event-stream')


@app.get('/ask') 
async def ask(question: str=None, prefers_streaming:bool = True, encode: bool = True, raw:bool=False):
    """
    entry point to ask some questions
    
    Args:
    
        encode: base 64 encoding is used to protect the newlines from the whims of EventSources (see 3. below)
        raw:  raw messages allow is to see that streaming would work with markdown except that Event Sources inject newlines that break the message
        prefers_streaming: can be disabled to test direct response
        

    Event Source / Stream should take a specific data format - HTMX builds on these as you can see...
    1. https://v1.htmx.org/extensions/server-sent-events/
    2. https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
    
    I experienced an issue when trying do markdown from event sources as that is why i base 64 encode.  this issues was also discussed here so i knew it was not just me
    3. https://medium.com/@thiagosalvatore/the-line-break-problem-when-using-server-sent-events-sse-1159632d09a0
                        
    """
    try:
        from src import agent
        
        """interact and respond"""
        if question:
            print(question)
            stream = agent(question)
            #we dont actually use the buffer but we could return a full message this way if we wanted
            buffer = []    
            def iterate_s():
                if not question:
                    yield buffer_term("".join(buffer))
                for s in stream: 
                    if s:
                        buffer.append(s)
                        if encode:
                            s = b64encode(s)
                        if not raw:
                            s = f"data: {s}\n\n"
                        yield s
                    else:
                        """to let the client know we are done we explicitly terminate using a different message
                           see how the client uses this to swap out the sse div
                        """
                        yield buffer_term("".join(buffer)) 

            return StreamingResponse(iterate_s(), media_type='text/event-stream') if prefers_streaming else Response(content=stream)

    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=str(ex))
  

