def response(prompt):


    client.pull('llama3.1')
    response = client.chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': f'{prompt}',
    },
    ])

    return response

with open("/root/AI-service/ai-service-group5/besluit_1.txt", "r") as f:
    text= f.read()

print(text)