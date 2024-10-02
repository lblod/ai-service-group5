import pandas as pd
from ollama import Client
from besluit import besluit_plaintext 

besluiten = besluit_plaintext 

client = Client(host='http://ollama:11434')

df = pd.read_csv("/root/AI-service/ai-service-group5/producten-data/producten_en_diensten_2024-09-13_21-47-37.csv", encoding="cp1252", encoding_errors="ignore")
thema = df['Thema(Õs)'].unique().tolist()
type = df['Type'].unique().tolist()
doelgroep = df['Doelgroep(en)'].unique().tolist()

prompt_doelgroep = f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    Here is the text: {besluiten}
                    For the content you are given, you need to classify according to this criteria: Doelgroep. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Doelgroep, refer to {doelgroep}. 
                    For the Doelgroep criteria, there can be multiple labels that can applied to the given text. 
                    **Return all of the relevant labels associated to the text.""" 

prompt_type = f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    Here is the text: {besluiten}
                    For the content you are given, you need to classify according to this criteria: Type. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Type, refer to {type}. 
                    For the Type criteria, there can be multiple labels that can applied to the given text. 
                    **Return the relevant label associated to the text. There is only one label that can be associated**. """

prompt_thema = f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    Here is the text: {besluiten}
                    For the content you are given, you need to classify according to this criteria: Thema. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Type, refer to {thema}. 
                    For the Thema criteria, there can be multiple labels that can applied to the given text. 
                    **Return the relevant label associated to the text. There is only one label that can be associated**. """




def get_target_group(prompt_doelgroep): 
    client.pull('llama3.1')
    response = client.generate(model='llama3.1', prompt=prompt_doelgroep)
    
    return response


def get_type(prompt_type): 
    client.pull('llama3.1')
    response = client.generate(model='llama3.1', prompt=prompt_type)
    
    return response


def get_thema(prompt_thema):
    
    client.pull('llama3.1')
    response = client.generate(model='llama3.1', prompt=prompt_thema)
    
    return response