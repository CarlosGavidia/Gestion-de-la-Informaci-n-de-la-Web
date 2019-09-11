# -*- coding: utf-8 -*-
 
#
#Carlos Gavidia Ortiz,Iván Monterrubio Cerezo,Sergio González Jiménez y José Antonio Bernal Pérez declaramos que esta solución
#es fruto exclusivamente nuestro trabajo personal. No hemos sido
#ayudados por ninguna otra persona ni hemos obtenido la solución de
#fuentes externas, y tampoco hemos compartido nuestra solución con
#nadie. Declaramos además que no hemos realizado de manera deshonesta
#ninguna otra actividad que pueda mejorar nuestros resultados
#ni perjudicar los resultados de los demás.
#

import bottle
from bottle import run, get, template, request
import os
import urllib.request
import hashlib
import json
from beaker.middleware import SessionMiddleware #Importante: instalar beaker-> pip install beaker

# Credenciales. 
# https://developers.google.com/identity/protocols/OpenIDConnect#appsetup
# Copiar los valores adecuados.
CLIENT_ID     = '626459746129-0j29cumhcgpkjl8p6c6bie31u7io71t2.apps.googleusercontent.com'
CLIENT_SECRET = 'BT2Y_NDOYWkBj04FRL29lN_8'
REDIRECT_URI  = "http://localhost:8080/token"


# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/protocols/OpenIDConnect#authenticatingtheuser
DISCOVERY_DOC = "https://accounts.google.com/.well-known/openid-configuration"


# Token validation endpoint para decodificar JWT
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/tokeninfo'


@get('/login_google')
def login_google():
 
    web_session = bottle.request.environ.get('beaker.session')
    web_session['state'] = hashlib.sha256(os.urandom(1024)).hexdigest()
    web_session.save()
    page = (json.loads(urllib.request.urlopen(DISCOVERY_DOC).read().decode("utf-8"))['authorization_endpoint'] + 
            '?client_id=' + CLIENT_ID + '&response_type=code&scope=' +urllib.request.quote('openid ', safe = '')+ 
            'email' + '&redirect_uri=' + REDIRECT_URI + '&state=' +web_session['state'])
    
    #Mostraremos un boton para redireccionar a la página de autenticación delegada de Google
    return template('logearse.tpl',page = page)
	
@get('/token')
def token():

    #Completamos la informacion del cliente
    cliente = urllib.parse.urlencode({'code':request.query.code,'client_id':CLIENT_ID,
                                      'client_secret':CLIENT_SECRET,'redirect_uri':REDIRECT_URI,
                                      'grant_type':'authorization_code'}).encode("utf-8")
    
    url = urllib.request.urlopen(json.loads(urllib.request.urlopen(DISCOVERY_DOC).read().decode("utf-8"))['token_endpoint'],cliente).read()
    js = json.loads(url.decode("utf-8"))

    # A continuacion envio a Google los datos del cliente para que me devuleva un JSON
    cliente = urllib.parse.urlencode({'id_token':js['id_token']}).encode("utf-8")
    js = json.loads(urllib.request.urlopen('https://www.googleapis.com/oauth2/v3/tokeninfo',cliente).read().decode("utf-8"))

   
    #Mostramos la bienvenida al usuario con el mail del js extraido
    return template('bienvenido.tpl',mail=js['email'])


if __name__ == "__main__":

    session_opts = {'session.type': 'file','session.cookie_expires': 300,'session.data_dir': './data','session.auto': True}
    app = SessionMiddleware(bottle.app(), session_opts)

    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(app=app, host='localhost',port=8080,debug=True)
