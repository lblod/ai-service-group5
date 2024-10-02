import ollama
# from ai_processor import (
#     get_product_ai, get_target_group_ai, get_themas_ai,
#     get_product_description_ai, get_product_conditions_ai,
#     get_product_procedures_ai, get_product_proofs_ai,
#     get_all_product_information_ai, get_product_cost_ai,
#     get_product_type_ai
# )

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


def insert_lpdc_service_instance():
    query_string = """
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix dc: <http://purl.org/dc/terms/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix dbpedia: <http://dbpedia.org/resource/>
prefix dbpedia-owl: <http://dbpedia.org/ontology/>
prefix dbpprop: <http://dbpedia.org/property/>
prefix wdprop: <http://www.wikidata.org/prop/direct/>
prefix ruben: <https://ruben.verborgh.org/profile/#>
prefix rubent: <https://www.rubensworks.net/#>
prefix schema: <http://schema.org/>
prefix bow: <https://betweenourworlds.org/ontology/>
prefix lc: <http://semweb.mmlab.be/ns/linkedconnections#>

insert data {
  graph <http://mu.semte.ch/graphs/organizations/5116efa8-e96e-46a2-aba6-c077e9056a96/LoketLB-LPDCGebruiker> {
    <https://ipdc.tni-vlaanderen.be/id/instantie/9ffb00ff-8907-4b6d-b8bc-84181f3fb4d52> a <https://productencatalogus.data.vlaanderen.be/ns/ipdc-lpdc#InstancePublicService> ;
            <http://mu.semte.ch/vocabularies/core/uuid> '''9ffb00ff-8907-4b6d-b8bc-84181f3fb4d52''';
            <http://purl.org/pav/createdBy> <http://data.lblod.info/id/bestuurseenheden/5116efa8-e96e-46a2-aba6-c077e9056a96>;
            <http://www.w3.org/ns/adms#status> <http://lblod.data.gift/concepts/review-status/concept-ai-gegenereerd>;
            <http://purl.org/dc/terms/title> '''Test minimaal product'''@nl, '''Test minimaal product'''@nl-BE-x-generated-formal, '''Test minimaal product'''@nl-BE-x-generated-informal;
            <http://purl.org/dc/terms/description> '''<p>Test minimaal product van een kraam op het openbaar domein (ambulante activiteit) heb je een toelating van de gemeente nodig. Een ambulante activiteit heeft betrekking op de verkoop, het te koop aanbieden of het uitstallen met het oog op de verkoop aan de consument van producten of diensten, door een handelaar buiten de vestiging vermeld in zijn inschrijving in de Kruispuntbank van Ondernemingen (KBO) of door een persoon die niet over zo’n vestiging beschikt. </p>'''@nl-BE-x-generated-informal, '''<p>Voor de uitbating van een kraam op het openbaar domein (ambulante activiteit) hebt u een toelating van de gemeente nodig. Een ambulante activiteit heeft betrekking op de verkoop, het te koop aanbieden of het uitstallen met het oog op de verkoop aan de consument van producten of diensten, door een handelaar buiten de vestiging vermeld in zijn inschrijving in de Kruispuntbank van Ondernemingen (KBO) of door een persoon die niet over zo’n vestiging beschikt. </p>'''@nl, '''<p>Voor de uitbating van een kraam op het openbaar domein (ambulante activiteit) hebt u een toelating van de gemeente nodig. Een ambulante activiteit heeft betrekking op de verkoop, het te koop aanbieden of het uitstallen met het oog op de verkoop aan de consument van producten of diensten, door een handelaar buiten de vestiging vermeld in zijn inschrijving in de Kruispuntbank van Ondernemingen (KBO) of door een persoon die niet over zo’n vestiging beschikt. </p>'''@nl-BE-x-generated-formal;
            <http://data.europa.eu/m8g/thematicArea> <https://productencatalogus.data.vlaanderen.be/id/concept/Thema/EconomieWerk>;
            <https://productencatalogus.data.vlaanderen.be/ns/ipdc-lpdc#targetAudience> <https://productencatalogus.data.vlaanderen.be/id/concept/Doelgroep/Burger>, <https://productencatalogus.data.vlaanderen.be/id/concept/Doelgroep/GezinMetKinderenOfJongeren>;
            <http://www.w3.org/ns/dcat#keyword> '''ambulante activiteit'''@nl, '''ambulante activiteiten'''@nl, '''ambulante handel'''@nl, '''openbaar domein'''@nl, '''foodtrucks'''@nl, '''foodtruck'''@nl, '''food truck'''@nl, '''standplaats'''@nl, '''marktkraam'''@nl;
            <http://schema.org/dateCreated> '''2023-03-09T15:40:24.123296327Z'''^^<http://www.w3.org/2001/XMLSchema#dateTime>;
            <http://schema.org/dateModified> '''2023-05-05T09:05:34.971218272Z'''^^<http://www.w3.org/2001/XMLSchema#dateTime>;
            <https://productencatalogus.data.vlaanderen.be/ns/ipdc-lpdc#isArchived> "false".
  }
}
    """
    update_sudo(query_string)



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

    insert_lpdc_service_instance()
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
                task_uri = task_res["results"]["bindings"][0]["uri"]["value"]
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
        if insert["predicate"]["value"] == "http://redpencil.data.gift/vocabularies/tasks/operation"
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
