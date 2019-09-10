# -*- coding: utf-8 -*-

##
#Carlos Gavidia Ortiz,Iván Monterrubio Cerezo,Sergio González Jiménez y José Antonio Bernal Pérez declaramos que esta solución
#es fruto exclusivamente nuestro trabajo personal. No hemos sido
#ayudados por ninguna otra persona ni hemos obtenido la solución de
#fuentes externas, y tampoco hemos compartido nuestra solución con
#nadie. Declaramos además que no hemos realizado de manera deshonesta
#ninguna otra actividad que pueda mejorar nuestros resultados
#ni perjudicar los resultados de los demás.
##

from bottle import *
from pymongo import MongoClient
import hashlib
import binascii
import random
import urllib
import onetimepass #Hay que tenerlo instalado
import urllib.parse# Necesario para lo de el codigo QR



#Todas las posibles combinaciones en la salt
SALT = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#Nos inventamos una pimienta
PEPPER = 'dsabdjDJSADBAS124763JDNSJas679sl1'


mongoclient = MongoClient()
db = mongoclient['giw']

##############
# APARTADO 1 #
##############

# 
# La seguridad para el hash de las contraseñas, deben ser suficientemente robustas
# para ataques como de fuerza bruta, que por ejemplo sha1 no lo resiste.
# Para un buen has de una contraseña, es necesario incluir una sal como hacemos en la práctica
# y además incluimos una pimineta para reforzarla.
# Es por tanto que usaremos la función: hashlib. pbkdf2_hmac ( hash_name , password , salt , iterations , dklen = None )
# Y que la proporciona PKCS # 5. Utilizaremos con hash_name el algoritmo sha256
# El número de iteraciones debe elegirse según el algoritmo hash y la potencia de cálculo. 
#A partir de 2013, se sugieren al menos 100.000 iteraciones de SHA-256, que será el que utilizamos en la práctica.
# Bibliografía: https://docs.python.org/3.5/library/hashlib.html
#

# Genera un secreto(semilla) aleatorio(para la parte 2)
def generateSecret():
    VALUES = "234567ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = []
    
    for i in range(16):
        s.append(random.choice(VALUES))
        
    secret = ''.join(s)
    return secret

@post('/signup')
def signup():

    # Cogemos los datos de la peticion POST
    nick = request.forms.get("nickname")
    name = request.forms.get("name")
    country = request.forms.get("country")
    email = request.forms.get("email")
    password = request.forms.get("password")
    password2 = request.forms.get("password2")

    # Si las contraseñas no coinciden se devuelve un error
    if password != password2:
        return template("errorPasswordDiferente.tpl")

    # Buscamos el usuario en la base de datos
    users = db.users.find({"_id": nick})

    # Si existe se devuelve un error
    if users.count() > 0:
        return template("errorUsuarioExistente.tpl")

    #Hacemos la sal
    saltNew=[]
    for i in range(64):
        saltNew.append(random.choice(SALT))

    saltNueva = ''.join(saltNew)
    password =password +PEPPER

    #Se aplica función hash
    dk = hashlib.pbkdf2_hmac('sha256', str.encode(password),  str.encode(saltNueva), 100000)
    password = binascii.hexlify(dk)

    # Guardamos el usuario en la base de datos
    insert = db.users.insert_one({
        "_id":nick,
        "name":name,
        "country":country,
        "email":email,
        "password":password,
        "salt":saltNueva
    })

    # Devolvemos la plantilla de bienvenida al nuevo usuario
    return template("welcome.tpl", nick=nick)

@post('/change_password')
def change_password():
    
    nickname = request.forms.get('nickname')
    old_password = request.forms.get('old_password')
    new_password = request.forms.get('new_password')

    #buscamos el nickname en nuestra base de datos:
    usuarios = db.users.find({'_id': nickname})

    #Si no lo encontramos al usuario o si la antigua contraseña no coincide mostramos el error
    if usuarios.count() != 1:
        return template("errorUsuarioContrasenia.tpl")

    #Como en la BBDD la contrasenia esta hasheada, primero la tenemos que obtener asi:
    
    #Obtenermos la sal del usuario:
    for i in usuarios:
        saltNick = str(i['salt'])
        passwordNick = i['password']

    #Se mete la pimienta
    old_password =old_password+PEPPER

    #Se aplica la función hash
    dk = hashlib.pbkdf2_hmac('sha256', str.encode(old_password),  str.encode(saltNick), 100000)
    old_passwordTrans = binascii.hexlify(dk)
    
    #Una vez conseguida la contraseña la comparamos con la que haya metido el usuario.
    if old_passwordTrans != passwordNick:
       return template("errorUsuarioContrasenia.tpl")

    #Cambiamos la contrasenia:
    #Se crea una sal
    saltNew=[]
    for i in range(64):
        saltNew.append(random.choice(SALT))

    saltNueva = ''.join(saltNew)

    #Se le mete la pimienta
    new_password = new_password+ PEPPER

    #Conseguimos el hash juntando todo
    dk = hashlib.pbkdf2_hmac('sha256', str.encode(new_password),  str.encode(saltNueva),100000)
    new_passwordTrans = binascii.hexlify(dk)

    #Se cambia la contrasenia en la BBDD
    consulta = db.users.update_one({'_id': nickname}, {'$set': {'password':new_passwordTrans, 'salt': saltNueva}})

    return template('contraseniaModificada.tpl',nickname=nickname)

            
@post('/login')
def login():
    nickname = request.forms.get('nickname')
    password = request.forms.get('password')
    
    #buscamos el nickname en nuestra base de datos:
    usuarios = db.users.find({'_id': nickname})

    #Si no lo encontramos al usuario o si la antigua contraseña no coincide mostramos el error
    if usuarios.count() != 1:
        return template("errorUsuarioContrasenia.tpl")

    #Como en la BBDD la contrasenia esta hasheada, primero la tenemos que obtener asi:
    
    #Obtenermos la sal del usuario:
    for i in usuarios:
        name = i['name']
        saltNick = str(i['salt'])
        passwordNick = i['password']

    #Se mete la pimienta
    password =password+PEPPER

    #Se aplica la función hash
    dk = hashlib.pbkdf2_hmac('sha256', str.encode(password),  str.encode(saltNick), 100000)
    password = binascii.hexlify(dk)
    
    #Una vez conseguida la contraseña la comparamos con la que haya metido el usuario.
    if password != passwordNick:
       return template("errorUsuarioContrasenia.tpl")


    return template('logeado.tpl',name=name)


##############
# APARTADO 2 #
##############

# 
# Se genera una semilla aleatoria en base 32,se alamacena en la BBDD, para que
# cuando se compruebe la identidad de un usuario, se genere y se compruebe que el
# usuario es quien es. La función para generar la semilla esta arriba del todo, que es
# parecida a la sal, cogemos aleatoriamente 16 digitos para hacerla.
#

@post('/signup_totp')
def signup_totp():
    
    nickname = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    password = request.forms.get('password')
    password2 = request.forms.get('password2')
    
    #Comprobamos primero si las contraseñas coinciden 
    if password != password2:
        return template("errorPasswordDiferente.tpl")
    
    #Si coinciden, consultamos la base de datos por si ese nick está cogido
    usuarios = db.users.find({'_id': nickname})
    
    if usuarios.count() == 1 :
        return template ("errorUsuarioExistente.tpl")
    #Si no existe, insertamos al nuevo usuario en la base de datos
    #Se hacela sal como antes
    #Se crea una sal
    saltNew=[]
    for i in range(64):
        saltNew.append(random.choice(SALT))

    saltNueva = ''.join(saltNew)
    password = password+PEPPER

    #Hacemos la funcion hash
    dk = hashlib.pbkdf2_hmac('sha256', str.encode(password),  str.encode(saltNueva), 100000)
    password = binascii.hexlify(dk)
    
    seed = generateSecret()
    
    db.users.insert_one({
            '_id': nickname,
            'name': name,
            'country': country,
            'email': email,
            'password': password, 
            'salt': saltNueva,
            'seed': seed
            })
    
    s_url = 'otpauth://totp/'+nickname+'?secret='+seed
    qr_url = 'http://api.qrserver.com/v1/create-qr-code/?data=' + urllib.parse.quote(s_url, safe = '')
    
    return template("vistaQR.tpl", name =name, semilla =seed, url = qr_url)
        
        
@post('/login_totp')        
def login_totp():
    
    nickname = request.forms.get('nickname')
    password = request.forms.get('password')
    totp = request.forms.get('totp')
    
    usuarios = db.users.find({'_id': nickname})
    
    if usuarios.count() != 1 :
        return template("errorUsuarioContrasenia.tpl")
        
    #Obtenermos al usuario:
    for i in usuarios:
        name = i['name']
        saltNick = str(i['salt'])
        passwordNick = i['password']
        seed = i['seed']

    password = password+PEPPER

    #Hacemos la funcion hash
    dk = hashlib.pbkdf2_hmac('sha256', str.encode(password),  str.encode(saltNick), 100000)
    password = binascii.hexlify(dk)
    
    #Una vez conseguida la contraseña la comparamos con la que haya metido el usuario.
    if password != passwordNick:
       return template("errorUsuarioContrasenia.tpl")
    
    #Validamos el TOTP
    valid_totp= onetimepass.valid_totp(token = totp, secret = seed)
    if valid_totp:
        return template("errorUsuarioContrasenia.tpl")
    else:
        return template('logeado.tpl',name=name)

    
if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)
