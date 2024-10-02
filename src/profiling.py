import pandas as pd
from llama_cpp import Llama


df = pd.read_csv("/root/AI-service/ai-service-group5/producten-data/producten_en_diensten_2024-09-13_21-47-37.csv", encoding="cp1252", encoding_errors="ignore")
thema = df['Thema(Õs)'].unique().tolist()
type = df['Type'].unique().tolist()
doelgroep = df['Doelgroep(en)'].unique().tolist()


llm = Llama.from_pretrained(
        repo_id="svercoutere/llama-3-8b-instruct-abb",
        filename="llama-3-8b-instruct-abb-unsloth.Q4_K_M.gguf",
        n_ctx=8192
    )


def get_target_group(besluiten): 
    
    response = llm.create_chat_completion(
    messages = [
        {"role": "assistant", 
        "content": f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    For the content you are given, you need to classify according to this criteria: Doelgroep. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Doelgroep, refer to {doelgroep}. 
                    For the Doelgroep criteria, there can be multiple labels that can applied to the given text. 
                    **Return all of the relevant labels associated to the text."""            
        },
        {
            "role":"user",
            "content":f"{besluiten}"
        }
    ]
    )
    return response['choices'][0]['message']['content']


def get_type(besluiten):
    
    
    thema = df['Thema(Õs)'].unique().tolist()
    type = df['Type'].unique().tolist()
    doelgroep = df['Doelgroep(en)'].unique().tolist()

    
    response = llm.create_chat_completion(
    messages = [
        {"role": "assistant", 
        "content": f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    For the content you are given, you need to classify according to this criteria: Type. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Type, refer to {type}. 
                    For the Type criteria, there can be multiple labels that can applied to the given text. 
                    **Return the relevant label associated to the text. There is only one label that can be associated**. """            
        },
        {
            "role":"user",
            "content":f"{besluiten}"
        }
    ]
    )
    return response['choices'][0]['message']['content']


def get_thema(besluiten):
    
    response = llm.create_chat_completion(
    messages = [
        {"role": "assistant", 
        "content": f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    For the content you are given, you need to classify according to this criteria: Thema. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Type, refer to {thema}. 
                    For the Thema criteria, there can be multiple labels that can applied to the given text. 
                    **Return the relevant label associated to the text. There is only one label that can be associated**. """           
        },
        {
            "role":"user",
            "content":f"{besluiten}"
        }
    ]
    )
    return response['choices'][0]['message']['content']