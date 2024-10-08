from ollama import Client
# from openai import OpenAI
# import mlflow
from prompts import (
    summary_prompt, product_prompt, prompt_description, prompt_title,
    prompt_conditions, prompt_procedure, prompt_justification,
    prompt_doelgroep, prompt_type, prompt_thema, prompt_multi_fields
)

client = Client(host='http://ollama:11434')


# mlflow.set_tracking_uri("http://mlflow:9292")
# mlflow.set_experiment("abb-hackathon")
# mlflow.openai.autolog()
# mlflow.set_run()

# OAIclient = OpenAI(
#         api_key = "ollama",
#         base_url = "http://ollama:11434/v1",
#         )

def llm_response(prompt):
    client.pull('llama3.1')
    
    response = client.generate('llama3.1', prompt)
    # response = OAIclient.chat.completions.create(
    #         model='llama3.1',
    #         messages = [
    #             { 'role': 'user',
    #               'content': 'prompt',}
    #             ])
    return response

# Function for API route
def get_product_ai(text):
    full_prompt = f"{product_prompt}\n\n{text}"
    return llm_response(full_prompt)

def get_target_group_ai(text):
    full_prompt = f"{prompt_doelgroep}\n\n{text}"
    return llm_response(full_prompt)

def get_themas_ai(text):
    full_prompt = f"{prompt_thema}\n\n{text}"
    return llm_response(full_prompt)

def get_product_description_ai(text):
    full_prompt = f"{prompt_description}\n\n{text}"
    return llm_response(full_prompt)

def get_product_conditions_ai(text):
    full_prompt = f"{prompt_conditions}\n\n{text}"
    return llm_response(full_prompt)

def get_product_procedures_ai(text):
    full_prompt = f"{prompt_procedure}\n\n{text}"
    return llm_response(full_prompt)

def get_product_proofs_ai(text):
    full_prompt = f"{prompt_justification}\n\n{text}"
    return llm_response(full_prompt)

def get_all_product_information_ai(text):
    product_name = get_product_ai(text)
    full_prompt = prompt_multi_fields.format(product_name=product_name, regulation=text)
    return llm_response(full_prompt)

def get_product_cost_ai(text):
    prompt = f"Extract the cost of the product from the following text: {text}"
    return llm_response(prompt)

def get_product_type_ai(text):
    full_prompt = f"{prompt_type}\n\n{text}"
    return llm_response(full_prompt)
