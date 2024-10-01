#import ollama

@app.route("/extract-voorwaarden")
def extract(dummy):
    return 'some value'

@app.route("/hello")
def hello():
    return "Hello from some template!"

@app.route("/bye")
def bye():
    return "goodbye"