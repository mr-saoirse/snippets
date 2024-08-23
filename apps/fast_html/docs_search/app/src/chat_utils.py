import json, openai, typing
from pydantic import BaseModel



"""
1 Setup some language model utils 
"""
GPT_MINI = "gpt-4o-mini"
DEFAULT_MODEL =  GPT_MINI# "gpt-4o-2024-08-06"

class FunctionCall(BaseModel):
    name: str
    arguments: str | dict


def _get_function_call_or_stream(
    response, callback=None, response_buffer=None, token_callback_action=None
):
    """
    This is a little bit opaque as it tries to abstract
    function calling and non-function calling for both streaming modes
    """

    def function_builder(function_call, response):
        """wrap it in our simple interface"""
        function_name = function_call.name
        function_args = function_call.arguments
        for c in response:
            if c.choices:
                c = c.choices[0].delta
                if c.function_call:
                    function_args += c.function_call.arguments
        return FunctionCall(name=function_name, arguments=json.loads(function_args))

    def content_builder(content, response):
        """
        isolate the code path where we return a generator
        """
       
        yield content
        for c in response:
            if c.choices:
                c = c.choices[0].delta
                yield c.content

    if isinstance(response, openai.Stream):
       
        """this just checks the different states of messages"""
        content = ""
        for chunk in response:
            #print(chunk)
            if chunk.choices:
                _chunk = chunk.choices[0].delta
                has_call = _chunk.function_call
                if has_call:
                    fb = function_builder(
                        _chunk.function_call,
                        response,
                    )
                    return fb
                
                elif _chunk.content:
                    """here we optionally stream to the callback"""
                    content += _chunk.content
                    if callback:
                        callback(_chunk.content)
                    # if isinstance(response_buffer, list):
                    #     response_buffer.append(_chunk.content)
                    # we go into generator mode when there is no callback and its a stream
                    else:
                        return content_builder(_chunk.content, response)
      

        if isinstance(response_buffer, list):
            response_buffer.append(content)
        return content

    else:
        """not streaming mode - respecting the same interface"""
        response_message = response.choices[0].message
        function_call = response_message.function_call
        if function_call:
            return FunctionCall(
                name=function_call.name,
                arguments=json.loads(function_call.arguments),
            )
        if isinstance(response_buffer, list):
            response_buffer.append(response_message.content)

        """not streaming mode token callback"""
        if token_callback_action:
            try:
                token_callback_action(response)
            except:
                raise

        return response_message.content

class VectorStore:
    def __init__(self):
        pass
    
    def __call__(self, question:str) -> typing.List[str]:
        """run a vector search"""
        return {"response": "actual there was nothing found just use general knowledge to answer the question"}
    

class GptModel:

    def get_function_call_or_stream(
        self,
        response: typing.Any,
        callback: typing.Optional[typing.Callable] = None,
        response_buffer: typing.List[typing.Any] = None,
        token_callback_action: typing.Optional[typing.Callable] = None,
    ):
        return _get_function_call_or_stream(
            response=response,
            callback=callback,
            response_buffer=response_buffer,
            token_callback_action=token_callback_action,
        )
        
    def __call__(self, question:str):
        """
        this agent takes the question and does a vector search 
        - just assume its a question about FastHTML to make the choices simpler here
        """
        store = VectorStore()
        
        GUIDE = f"""
        You are given the results of a vector search below to answer the users question. 
        Please response to the user
        
        ## Users question
        ```text
        {question}
        ```
        
        ## Search Results
        ```json
        {json.dumps(store(question),default=str)}
        ```
        
        """
        
        messages = [{
            'role': 'user', 'content': GUIDE
        }]
        
        return self.run(messages)
    

    def run(
        cls,
        messages: typing.List[dict],
        is_streaming: bool = True,
        functions: typing.Optional[dict] = None,
        callback: typing.Callable = None,
        **kwargs
    ):
        """
        Ask question with possible function usage
        """

        response = openai.chat.completions.create(
            model=DEFAULT_MODEL,
            functions=(list(functions) if functions else None),
            function_call="auto" if functions else None,
            messages=messages,
            temperature=0,
            response_format=None,
            stream=is_streaming,
            stream_options=({"include_usage": True} if is_streaming else None),
        )

        cls.response_buffer = []
        response = _get_function_call_or_stream(
            response,
            callback,
            response_buffer=cls.response_buffer, 
        )

        return response

agent = GptModel()

"""
2 Scrape the help pages for Fast HTML and insert them
"""