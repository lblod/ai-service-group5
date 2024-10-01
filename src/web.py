import ollama

from ollama import Client

client = Client(host='http://ollama:11434')


@app.route("/hello")
def hello():
    return "Hello from our template!"

@app.route("/bye")
def bye():
    return "goodbye"
@app.route("/ollama-summarize")
def response():


    client.pull('llama3.1')
    response = client.chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
    ])

    return response

@app.route("/ollama-extract")
def extract():
    return