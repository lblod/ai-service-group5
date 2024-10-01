from fastapi import FastAPI
import gradio as gr
import ollama


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

def complete(system_prompt, prompt, text):

    comb_prompt = f'''{prompt}

    ------------------------
    Document: {text}
    '''



    #print(comb_prompt)
    response = client.chat(model="llama3.1", messages=[
            { 'role': 'system',
              'content': system_prompt,},
            { 'role': 'user',
             'content': comb_prompt}
        ])
    return response['message']['content']



with gr.Blocks() as testblock:

    system_prompt = gr.Textbox(label="system prompt", show_label=True)
    user_prompt = gr.Textbox(label="user prompt", show_label=True)
    besluit = gr.Textbox(label="besluit", show_label=True)

    output = gr.Textbox(label="output", show_label=True)

    submit_button = gr.Button(value='submit')
    
    submit_button.click(complete, inputs=[system_prompt, user_prompt, besluit], outputs = [output])

#test = gr.Interface( fn = complete, inputs=['text', 'text'], outputs=['text'])


app = gr.mount_gradio_app(app, demo, CUSTOM_PATH)
app = gr.mount_gradio_app(app, testblock, TEST_PATH)
