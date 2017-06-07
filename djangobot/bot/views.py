
from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import requests
from django.utils import encoding
from sys import argv
from wit import Wit

from .settings import Chaves

#url api
FB_URL_API = 'https://graph.facebook.com/me/messages?'

#WIT_TOKEN = 'Token de verificação wit.ai'

#FB_PAGE_TOKEN = 'Token que o Facebook fornece para a página que nosso app estivier associado'

#FB_VERIFY_TOKEN = 'Token da página para Facebook'


def index(request):
    return render(request, 'index.html', {})

class webhook(APIView):

    def get(self, request, format=None):
        # Webhook retorna a verificação

        verify_token = request.GET.get('hub.verify_token')
        # check checa se o token bate
        if verify_token == Chaves.FB_VERIFY_TOKEN:
            challenge = request.GET.get('hub.challenge')
            return Response(challenge)
        else:
            return Response('Requisição inválida')

            
    def post(self, request, format=None):
        #Handler do webhook (postback e messages)
        data = request.data

        if data['object'] == 'page':
            for entry in data['entry']:                
                messages = entry['messaging']
                if messages[0]:
                    message = messages[0]
                    fb_id = message['sender']['id']
                    if message['message'] != None:
                        text = message['message']['text']

                        botmsg = client.run_actions(session_id = fb_id,message = text)

                        return Response('Funcionou '+ fb_id +' ')
                    elif message['postback'] != None:
                        return Response('Postback')
                else:
                    return Response('Mensagem vazia')
        else:
            return Response('Evento diferente de objeto')
        

def fb_message(sender_id, text):
    #Função para retornar resposta ao messenger
    botmsg = encoding.smart_text(text, encoding = 'utf-8',strings_only=False,errors='strict')

    data = {
        'recipient': {'id': sender_id},
        'message':{'text':botmsg}
    }

    qs = 'access_token='+ Chaves.FB_PAGE_TOKEN
    # Envia POST request para o messenger
    resp = requests.post(FB_URL_API+qs,json=data)
  
    return resp.content
  

def send(request, response):
    # Sender function
    
    # Usamos fb_id como session_id
    fb_id = request['session_id']
    text = response['text']
    # envia message
    fb_message(fb_id, text)

    return response['text']


actions = {
    'send': send,    
}

# Setup Wit Client
client = Wit(access_token=Chaves.WIT_TOKEN, actions=actions)
