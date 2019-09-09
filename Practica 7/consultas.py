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

from pymongo import MongoClient
from bottle import *


mongoclient = MongoClient()
db = mongoclient['giw']
c = db['usuarios'] 
    
@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&&surname=Romero&birthdate=2006-08-14
    
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0:
        return template("errorParametrosVacio.tpl")
    
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "name" and parametro != "surname" and parametro != "birthdate":
            parametrosMalos.append(parametro)
        
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    #Guardamos el name, surname y birthdate(las que existan de esas)
    name=request.query.name
    surname=request.query.surname
    birthdate=request.query.birthdate
    
    #Hay diferentes consultas posibles:
    if len(name) == 0 and len(surname)==0 and len(birthdate)!=0:
        consulta = c.find({"birthdate":birthdate})

    elif len(name) == 0 and len(surname)!=0 and len(birthdate)==0:
        consulta = c.find({"surname":surname})

    elif len(name) == 0 and len(surname)!=0 and len(birthdate)!=0:
        consulta = c.find({"surname":surname,"birthdate":birthdate})

    elif len(name) != 0 and len(surname)==0 and len(birthdate)==0:
        consulta = c.find({"name":name})

    elif len(name) != 0 and len(surname)==0 and len(birthdate)!=0:
        consulta = c.find({"name":name,"birthdate":birthdate})

    elif len(name) != 0 and len(surname)!=0 and len(birthdate)==0:
        consulta = c.find({"name":name,"surname":surname})

    elif len(name) != 0 and len(surname)!=0 and len(birthdate)!=0:
        consulta = c.find({"name":name,"surname":surname,"birthdate":birthdate})
    
    print(consulta.count())
    #Le pasamos la consulta que hayamos generado
    return template("consulta.tpl", consulta=consulta) 

@get('/find_email_birthdate')
def email_birthdate():
    #http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    
    parametrosMalos=[]

    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0:
        return template('errorParametrosVacio.tpl')
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "from" and parametro != "to":
            parametrosMalos.append(parametro)
        
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template('errorParametrosIncorrectos.tpl', parametrosMalos=parametrosMalos)
    
    #Guardamos el name, surname y birthdate(las que existan de esas)
    fromDate=request.query["from"]
    toDate=request.query.to
    
    if len(fromDate) == 0 or len(toDate) == 0:
        return template('errorParametrosVacio.tpl')
    elif len(fromDate) != 0 and len(toDate) != 0:
        consulta = c.find({"birthdate": {"$gte": fromDate, "$lte": toDate}})
    

    #Le pasamos la consulta que hayamos generado
    return template("consulta.tpl", consulta=consulta)

@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    #http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    
    #Hacemos las mismas comprobaciones que en el apartado 1:
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0:
        return template("errorParametrosVacio.tpl")
    
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "country" and parametro != "likes" and parametro != "limit" and parametro != "ord":
            parametrosMalos.append(parametro)
        
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    #Guardamos todas las variables que nos den:
    country = request.query.country
    likes = request.query.likes
    listaLikes=likes.split(",")#metemos cada aficion en la lista, diciendo que lo que delimita es la 'coma'
    limit = request.query.limit
    if request.query.limit == "desc":
        orden = -1
    else:
        orden = 1
    
    #Primero vemos quienes coinciden para un pais, y luego si en sus gustos están en la lista creada
    #Además lo ordenamos por fecha segun nos haya dicho el usuario y ponemos el límite que nos haya dicho también
    consulta = c.find({"likes":{"$all":listaLikes},"address.country":country}).sort("birthdate", orden).limit(int(limit))
    #Llamamos al mismo template del punto1,para mostrar todos los campos
    return template("consulta.tpl", consulta=consulta) 

@get('/find_birth_month')
def find_birth_month():
    # http://localhost:8080/find_birth_month?month=abril
    parametrosMalos=[]

    dicMeses = dict()
    dicMeses["enero"] = "01"
    dicMeses["febrero"] = "02"
    dicMeses["marzo"] = "03"
    dicMeses["abril"] = "04"
    dicMeses["mayo"] = "05"
    dicMeses["junio"] = "06"
    dicMeses["julio"] = "07"
    dicMeses["agosto"] = "08"
    dicMeses["septiembre"] = "09"
    dicMeses["octubre"] = "10"
    dicMeses["noviembre"] = "11"
    dicMeses["diciembre"] = "12"
    
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0:
        return template('errorParametrosVacio.tpl')
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "month":
            parametrosMalos.append(parametro)
        
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template('errorParametrosIncorrectos.tpl', parametrosMalos=parametrosMalos)
    
    #Guardamos el name, surname y birthdate(las que existan de esas)
    mes=request.query.month
    
    if not mes in dicMeses:
        return template('errorParametrosIncorrectos.tpl', parametrosMalos=mes)
    
    if len(mes) == 0:
        return template('errorParametrosVacio.tpl')
    elif len(mes) != 0:
        numMes = dicMeses[mes]
        numMes = "-" + numMes + "-"
        consulta = c.find({"birthdate": {"$regex": numMes}}).sort([("birthdate", 1)])
    

    #Le pasamos la consulta que hayamos generado
    return template("consulta.tpl", consulta=consulta)
    
@get('/find_likes_not_ending')
def find_likes_not_ending():
  # http://localhost:8080/find_likes_not_ending?ending=s
    #Realizamos las mismas comprobaciones que en el resto de apartados
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0:
        return template("errorParametrosVacio.tpl")
    
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "ending":
            parametrosMalos.append(parametro)
        
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    #Guardamos el sufijo
    ending=request.query.ending
    #ending=ending.lower()
    
    #Realizamos la consulta usando /.*cadena.*/ donde las barras son equivalentes
    #al like en SQL y el .* equivale a %
    consulta = c.find({"likes": {'$not':re.compile(ending+"$", re.IGNORECASE)}})
    #consulta = c.find({"likes": {'$regex' : '^((?!ending).)*$', '$options' : 'i'}})
    #db.products.find( { sku: { $regex: /^ABC/i } } )
    #https://docs.mongodb.com/manual/reference/operator/query/regex/#op._S_regex
    
    #Llamamos al mismo template del punto1,para mostrar todos los campos
    return template("consulta.tpl", consulta=consulta)


@get('/find_leap_year')     
def find_leap_year():
  # http://localhost:8080/find_leap_year?exp=20
    #Comprobamos parametros disponibles; si no hay, lanzamos error
    if len(request.query)==0:
        return template("errorParametrosVacio.tpl")
    
    # Analizamos parametros disponibles; si no son adecuados, lanzamos error
    for parametro in request.query:
        if parametro != "exp":
            l = []
            l.append(parametro)
            return template("errorParametrosIncorrectos.tpl",parametrosMalos=l)
    
    exp = request.query.exp
    
    # Analizamos parametro, si tiene un formato erroneo, lanzamos error
    if len(str(exp))!=2:
        l = ["exp"]
        return template("errorParametrosIncorrectos.tpl",parametrosMalos=l)
    
    # Funcion JavaScript para detectar años bisiestos en fechas de nacimiento
    jsFunc = "function(){"
    jsFunc = jsFunc + "     if('birthdate' in this){"
    jsFunc = jsFunc + "            let s = this['birthdate'];"
    jsFunc = jsFunc + "            let lis = s.split('-');"
    jsFunc = jsFunc + "            let year = lis[0];"
    jsFunc = jsFunc + "            if(year%4==0 && (year%100!=0 || year%400==0)) return true;"
    jsFunc = jsFunc + "            else return false;"
    jsFunc = jsFunc + "        }"
    jsFunc = jsFunc + "        else return false;"
    jsFunc = jsFunc + "}"
    
    # Consultamos con pymongo los usuarios cuya año de caducidad de la tarjeta de credito es exp
    # y si su año de nacimiento es bisiesto
    consulta = c.find({"credit_card.expire.year":exp,"$where":str(jsFunc)})
    
    # Devolvemos la plantilla con el resultado adecuado
    return template("consulta.tpl", consulta=consulta)

###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)