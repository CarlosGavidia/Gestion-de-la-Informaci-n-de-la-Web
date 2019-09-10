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

#Tener el mongod abierto
#abrir un cmd aparte e ir a la carpeta donde estan los archivos json:
# cd C:\Users\gavo9\Desktop\UCM\4 curso Ingenieria Informatica\GIW\Practica9
#Para importar los json:
# mongoimport --db giw --collection usuarios --file usuarios.json
# mongoimport --db giw --collection pedidos --file pedidos.json
from pymongo import MongoClient
from bottle import *

mongoclient = MongoClient()
db = mongoclient['giw']

@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def agg1():
   
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    n = request.query.n
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "n" or int(n) < 1:
            parametrosMalos.append(parametro)
    
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0 :
        return template("errorParametrosVacio.tpl")

    consulta = db.usuarios.aggregate([{"$group": {"_id":"$pais","numUsuarios":{"$sum": 1}}},
                                      {"$sort": {"numUsuarios":-1,"_id":1}},
                                      {"$limit": int(n)}])

    return template('paisesMaxUsuarios.tpl',consulta=consulta)

@get('/products')
# http://localhost:8080/products?min=2.34
def agg2():
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "min":
            parametrosMalos.append(parametro)
    
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    min = request.query.min
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0:
        return template("errorParametrosVacio.tpl")

    consulta = db.pedidos.aggregate([{"$unwind":"$lineas"},
                                     {"$match":{"lineas.precio":{"$gte":float(min)}}},
                                     {"$group":{"_id": "$lineas.nombre", "unidades": {'$sum': '$lineas.cantidad'},"precioUnitario": {"$first": "$lineas.precio"}}}])

    return template('productos.tpl',consulta=consulta)
    
@get('/age_range')
# http://localhost:8080/age_range?min=80
def agg3():
    
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "min":
            parametrosMalos.append(parametro)
    
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    min = request.query.min
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0 or int(min) < 1:
        return template("errorParametrosVacio.tpl")

    consulta = db.usuarios.aggregate([
            {"$group": {"_id":"$pais","numUsuarios":{"$sum": 1},"maxAge":{"$max": "$edad"}, "minAge":{"$min": "$edad"}}},
            {"$match" : {"numUsuarios":{"$gt": int(min)}}},
            {"$project": {"rangoEdad":{"$subtract": ["$maxAge","$minAge"]}, 'numUsers': 1}},
            {"$sort": {"rangoEdad":-1,"_id":1}}
            ])
    
    

    return template('rangoEdadesPaisesConMasDeMinUsuarios.tpl',consulta=consulta)
    
    
@get('/avg_lines')
# http://localhost:8080/avg_lines
def agg4():
    c = db['usuarios']
    
    consulta = c.aggregate([{"$lookup": {"from" : "pedidos","localField" : "_id","foreignField" : "cliente","as" : "pedidosXCliente"}},
                            {"$unwind" : "$pedidosXCliente"},
                            {"$group": {"_id" : "$pais","lineasPromedio" : {"$avg" : {"$size" : "$pedidosXCliente.lineas"}}}}])
    
    return template('mediaPedidosXPais.tpl',consulta=consulta)
    
    
@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def agg5():
    #Hago una lista con los argumentos  malos si los hubiese,para mostrarlo por pantalla
    parametrosMalos=[]
    c = request.query.c
    
    for parametro in request.query:
        #Si algun paramtro no coincide nos vamos al template error de paramtros equivocados
        if parametro != "c":
            parametrosMalos.append(parametro)
    
    #Si el usuario ha metido parámetros incorrectos, se lo mostrarmos por pantalla
    if len(parametrosMalos)!=0:
        return template("errorParametrosIncorrectos.tpl", parametrosMalos=parametrosMalos)
    
    
    #Comprobamos si hay algo por parametro, si no la hay error
    if len(request.query)==0 or str(c) == "":
        return template("errorParametrosVacio.tpl")

    consulta = db.usuarios.aggregate([{"$lookup": {"from" : "pedidos", "localField" : "_id", "foreignField" : "cliente", "as" : "pedidos"}},
                                      {"$unwind" : "$pedidos"},
                                      {"$match": {"pais":{"$eq" : str(c)}}},
                                      {"$group": {"_id":"$pais","eurGastados":{"$sum":"$pedidos.total"}}}])

    return template('totalGastadoPorPais.tpl',consulta=consulta)
    
    
        
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
