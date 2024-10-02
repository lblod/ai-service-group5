from fastapi import FastAPI
import gradio as gr
import ollama
import openai
from openai import OpenAI
import mlflow

mlflow.set_tracking_uri("http://mlflow:9292")
mlflow.openai.autolog(log_models=True, log_model_signatures=True, log_traces=True, registered_model_name='llama3.1')
mlflow.set_experiment('abb-hackathon')
mlflow.start_run()

OAIClient = OpenAI( api_key="ollama", base_url="http://ollama:11434/v1")
#mlflow.openai.log_model(OAIClient, task='chat.completions', artifact_path='/mlruns')

#client = mlflow.openai.load






client = ollama.Client(host="http://ollama:11434")

#client.pull("llama3:instruct")

app = FastAPI()
CUSTOM_PATH = "/gradio"
TEST_PATH = "/test"

def greet(name, surname):
    return f"hello {name} {surname}"

demo = gr.Interface(
        fn = greet,
        inputs=['text', 'text'],
        outputs=['text'],
        )

def complete(system_prompt, text):

    comb_prompt = f'''{text}
    '''

    response = OAIClient.chat.completions.create(model="llama3.1", messages=[
            { 'role': 'system',
              'content': system_prompt,},
            { 'role': 'user',
             'content': comb_prompt}
        ])
    return response.choices[0].message.content


    #print(comb_prompt)
    #response = client.chat(model="llama3.1", messages=[
            #{ 'role': 'system',
              #'content': system_prompt,},
            #{ 'role': 'user',
             #'content': comb_prompt}
        #])
    #return response['message']['content']



with gr.Blocks() as testblock:

    system_prompt = gr.Textbox(label="system prompt", show_label=True)
    besluit = gr.Textbox(label="besluit", show_label=True)

    output = gr.Textbox(label="output", show_label=True)

    submit_button = gr.Button(value='submit')
    
    submit_button.click(complete, inputs=[system_prompt, besluit], outputs = [output])

#test = gr.Interface( fn = complete, inputs=['text', 'text'], outputs=['text'])


app = gr.mount_gradio_app(app, demo, CUSTOM_PATH)
app = gr.mount_gradio_app(app, testblock, TEST_PATH)
