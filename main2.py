import openai

api_key= 'YOUR API KEY HERE'

openai.api_key=api_key

def chatGTPResponse(conversation):
    try:
        response = openai.ChatCompletion.create( model='gpt-3.5-turbo', messages =conversation)
    except openai.error.APIConnectionError:
        return None

    conversation.append({'role': response.choices[0].message.role,'content':response.choices[0].message.content})
    return conversation

def initializeConversation():
    global conversation
    conversation = []
    conversation.append({'role':'system','content':'how may i help you?'})
    conversation = chatGTPResponse(conversation)