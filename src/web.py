import ollama
from flask import request, jsonify
from ollama import Client
from flask import jsonify, request
from rdflib import Graph
import threading
import os

from task import run_task, find_actionable_task_of_type
from helpers import logger, generate_uuid

from file import construct_insert_file_query, construct_get_file_query, shared_uri_to_path
from query_util import result_to_records
from sudo_query import query_sudo, update_sudo, auth_update_sudo

MY_TASK_TYPE = "http://lblod.data.gift/id/jobs/concept/TaskOperation/ai-extraction"
MY_EXTRACTION_GRAPH = ""

client = Client(host='http://ollama:11434')

class DeltaHandling:
    def __init__(self) -> None:
        self.mutex = threading.Lock()

delta_handling = DeltaHandling()

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


# TODO: move this out of web.py
def run_extraction_task(source_file_uri):
    file_query = construct_get_file_query(source_file_uri, None)
    query_result = query_sudo(file_query)
    file = result_to_records(query_result)[0]

    file_path = shared_uri_to_path(file["physicalFile"])
    with open(file_path, "r") as f:
        contents = f.read()
    logger.debug("Got contents of source file")
    logger.debug(contents)

    extraction_result = "My results"
    # TODO: write results to Triplestore

    logger.debug("Ending extraction")
    # Only return something if you want a resultscontainer.
    # We don't we just want to add some content to the triplestore for now.
    return None


def run_pending_tasks():
    with delta_handling.mutex:
        while True:
            task_q = find_actionable_task_of_type(MY_TASK_TYPE, None)
            task_res = query_sudo(task_q)
            if task_res["results"]["bindings"]:
                task_uri = task_res["results"]["bindings"][0]["job"]["value"]
                result = run_task(task_uri, MY_EXTRACTION_GRAPH, lambda sources: [run_extraction_task(sources[0])], query_sudo, update_sudo)
                if result:
                    logger.debug("We have an AI result to work with!")
            else:
                break

@app.route("/delta", methods=["POST"])
def handle_delta():
    # Only trigger in case of extraction job insertion
    request_data = request.get_json()
    inserts, *_ = [
        changeset["inserts"] for changeset in request_data if "inserts" in changeset
    ]
    new_extraction_jobs = [
        insert["subject"]["value"]
        for insert in inserts
        if insert["predicate"]["value"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        and insert["object"]["value"] == MY_TASK_TYPE
    ]
    if not new_extraction_jobs:
        return jsonify({"message": "Delta didn't contain new extraction jobs. Ignoring."})

    if delta_handling.mutex.locked():
        return jsonify({"message": "Extraction already in processs, the new job will be processed down the line."})

    new_thread = threading.Thread(target=run_pending_tasks)
    new_thread.start()
    logger.debug("Searching for pending extraction jobs.")
    return jsonify({"message": "Running pending extraction jobs."})
