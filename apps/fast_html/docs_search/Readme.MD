# Fast HTML Guide

This repo accompanies the article [here](https://medium.com/@mrsirsh/first-encounter-with-fasthtml-building-a-fasthtml-assistant-fe896d3a3e60)

It is created to illustrate getting started with FastHTML or rather, going beyond the basics to try and do things such as Server Sent Events as well as some basic styling and scripting. This Readme explains how to run the code and explains where the associated data came from. 

If you want to run the full sample with the doc Q&A be sure to set your Open AI key as an env variable as its used in OpenAI code in the utils. 
If you do not have an API key and dont want to get one, until I update this sample with more agents (e.g. Groq or LLama) you can use the dummy endpoint instead
## Running the sample

You can use poetry to run the samples or install the requirements e.g. `poetry install, poetry shell` or generate requirements and install into a virtual environment `poetry export -f requirements.txt --output requirements.txt --without-hashes`

This sample uses a server and client app both found in the app folder and steps depend on how you choose to install. Below I will just illustrate that we need to run both the server and client locally on dedicated ports.

**Server**
```bash
cd app
#run the server from the app folder in a terminal
#the swagger docs will be http://127.0.0.1:5009/docs
uvicorn server:app --port 5009 --reload

```

**Testing the server directly e.g. in a Jupyter notebook:** If you want to make sure the server is doing its thing, you can use the following sample code. You can test with swagger to just check its working but to simulate streaming you should use the code below to print out the stream

```python
import requests

with requests.get(
    'http://127.0.0.1:5009/ask?raw=true&encode=false',
    params={'question' : "please give an example of Seamus Heaney's poems with some example versus"}
) as r:
    for chunk in r.iter_content(1024):  # or, for line in r.iter_lines():
        print(chunk.decode(), end="")
```

or curl...

```bash

curl -X 'GET' \
  'http://127.0.0.1:5009/ask?question=capital%20of%20ireland&prefers_streaming=true&encode=false&raw=true' \
  -H 'accept: application/json'
```



**Client**

```bash
cd app
#run the FastHTML app from the app folder - runs on 5008 which is important for the CORS setting on the server
python main.py
```

## About the data

I scrapped the FastHTML docs into a vector store using the code in the utils and the LanceDB embedded database is included with the sample in `data` folder.
The agent will query the store and use GPT-mini by default to generate the answer. You can see this in the notebook


## interesting things


