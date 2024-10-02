import ollama
from flask import Flask, request, jsonify
from ollama import Client
from ai_processor import (
    get_product_ai, get_target_group_ai, get_themas_ai,
    get_product_description_ai, get_product_conditions_ai,
    get_product_procedures_ai, get_product_proofs_ai,
    get_all_product_information_ai, get_product_cost_ai,
    get_product_type_ai
)


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

@app.route("/get_product", methods=['POST'])
def get_product():
    text = request.json.get('text', '')
    result = get_product_ai(text)
    return jsonify({"product": result})

@app.route("/get_target_group", methods=['POST'])
def get_target_group():
    text = request.json.get('text', '')
    result = get_target_group_ai(text)
    return jsonify({"target_group": result})

@app.route("/get_themas", methods=['POST'])
def get_themas():
    text = request.json.get('text', '')
    result = get_themas_ai(text)
    return jsonify({"themas": result})

@app.route("/get_product_description", methods=['POST'])
def get_product_description():
    text = request.json.get('text', '')
    result = get_product_description_ai(text)
    return jsonify({"description": result})

@app.route("/get_product_conditions", methods=['POST'])
def get_product_conditions():
    text = request.json.get('text', '')
    result = get_product_conditions_ai(text)
    return jsonify({"conditions": result})

@app.route("/get_product_procedures", methods=['POST'])
def get_product_procedures():
    text = request.json.get('text', '')
    result = get_product_procedures_ai(text)
    return jsonify({"procedures": result})

@app.route("/get_product_proofs", methods=['POST'])
def get_product_proofs():
    text = request.json.get('text', '')
    result = get_product_proofs_ai(text)
    return jsonify({"proofs": result})

@app.route("/get_all_product_information", methods=['POST'])
def get_all_product_information():
    text = request.json.get('text', '')
    result = get_all_product_information_ai(text)
    return jsonify({"information": result})

@app.route("/get_product_cost", methods=['POST'])
def get_product_cost():
    text = request.json.get('text', '')
    result = get_product_cost_ai(text)
    return jsonify({"cost": result})

@app.route("/get_product_type", methods=['POST'])
def get_product_type():
    text = request.json.get('text', '')
    result = get_product_type_ai(text)
    return jsonify({"type": result})

