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
from mongoengine import *
import re

connect('giw_mongoengine')

class Producto(Document):
    codigoBarras=StringField(primary_key=True, min_length=13, max_length=13, regex="^[0-9]{13}$")
    nombre=StringField(required=True, min_length=1)
    catPrincipal=IntField(required=True)
    catSecundarias=ListField(IntField())
    def clean(self):
        #Primero se valida el formado del codigo de barras
        total = 0
        for i, digit in enumerate(reversed(self.codigoBarras[:-1])):
            total += int(digit) * 3 if (i % 2 == 0) else int(digit)
    
        digitoControl=(10 - (total % 10)) % 10

        if str(digitoControl)!=self.codigoBarras[-1]:
            raise ValidationError("El digito de control no es adecuado")
        #añadir a las categorias secundarias la categoria principal, al principio
        if len(self.catSecundarias) != 0:
            self.catSecundarias.insert(0,self.catPrincipal)

            
class TarjetaCredito(EmbeddedDocument):
	# Nombre completo del propietario de la tarjeta
	nombreCompleto = StringField(required=True)
	# Código de 16 cifras unico de cada tarjeta
	idTarjeta = StringField(unique=True, min_lenght = 16, max_lenght = 16)
	# Sólo desde Enero a Diciembre
	mesCaducidad = IntField(required=True, min_value = 1, max_value = 12)
	# Sólo años a partir del actual y de 4 cifras
	anioCaducidad = IntField(required=True, min_value = 2017, max_value = 9999)
	# CVV tipo StringField para poder fijar el nº de cifras a 3 y poder tener códigos que empiezan por 0
	cvv = StringField(required=True, min_lenght = 3, max_lenght = 3)
    
class LineaDePedido(EmbeddedDocument):
    cantidadProductos = IntField(required=True, min_value = 1)
    precioProducto = FloatField(required=True, min_value = 0)
    nombreProducto = StringField(required=True)
    precioTotalLinea = FloatField(required=True, min_value = 0)
    producto = ReferenceField(Producto, required=True)
        
    def clean(self):
        if self.precioTotalLinea != self.cantidadProductos * self.precioProducto:
            raise ValidationError("El precio total de la linea de pedido se ha calculado incorrectamente")
        if self.nombreProducto != self.producto.nombre:
            raise ValidationError("El nombre del producto es incorrecto")
            
        
class Pedido(Document):
    precioTotalPedido = FloatField(required=True, min_value = 0)
    fecha = ComplexDateTimeField(required=True)
    listaPedidos = ListField(EmbeddedDocumentField(LineaDePedido), required=True)
        
    def clean(self):
        total = 0
        for pedido in self.listaPedidos:
            total += pedido.precioTotalLinea
            
        if self.precioTotalPedido != total:
            raise ValidationError("El precio total del pedido se ha calculado incorrectamente")        
class Usuario(Document):
    #La expresion que esta donde el dni nos dice que encuentra un una secuencia de 8 digitos
    # y el ultimo es una letra entre la A y la Z.
    dni= StringField(primary_key=True, regex = "(\d{8}[A-Z])")
    #Ponemos min_lengh a 1 para que ponga algo en nombre y apellido
    nombre = StringField(required=True, min_lengh=1)
    primerApellido = StringField(required=True, min_lengh=1)
    segundoApellido = StringField(min_lengh=1)
    #como no existe un campo que solo sea fecha, sin horas ni minutos
    fechaNacimiento = StringField(required=True, regex = "\d{4}-\d{2}-\d{2}")
    #el campo ComplexDateTimeField() aparte de la fecha, tambien tiene hora, minutos, segundos
    ultimosAccesos = ListField(ComplexDateTimeField())
   
    tarjetasCredito = ListField(EmbeddedDocumentField(TarjetaCredito))
    pedidos = ListField(ReferenceField(Pedido))
    def clean(self):

       #Diccionario, de todas las letras posibles
        letrasDNI = dict()
        letrasDNI[0] = "T"
        letrasDNI[1] = "R"
        letrasDNI[2] = "W"
        letrasDNI[3] = "A"
        letrasDNI[4] = "G"
        letrasDNI[5] = "M"
        letrasDNI[6] = "Y"
        letrasDNI[7] = "F"
        letrasDNI[8] = "P"
        letrasDNI[9] = "D"
        letrasDNI[10] = "X"
        letrasDNI[11] = "B"
        letrasDNI[12] = "N"
        letrasDNI[13] = "J"
        letrasDNI[14] = "Z"
        letrasDNI[15] = "S"
        letrasDNI[16] = "Q"
        letrasDNI[17] = "V"
        letrasDNI[18] = "H"
        letrasDNI[19] = "L"
        letrasDNI[20] = "C"
        letrasDNI[21] = "K"
        letrasDNI[22] = "E"
        
        #Conseguimos todos los numeros de dni
        digitos = re.search("\d+", self.dni)
        #los agrupamos y lo pasamos a entero
        numero= int(digitos.group(0))
        #Indice del diccionario donde tiene que estar la letra que coincide con el DNI
        posicion=numero % 23
        #Conseguimos la letra
        letra = self.dni[-1]
     
        #Comparamos la letra que tiene que ser, con la letra que ha puesto el usuario
        #Si no coincide: ERROR
        if letrasDNI[posicion] != letra:
            raise ValidationError("Error. El DNI no es correcto")
     
        #Nos aseguramos que el DNI sean los 10 ultimos accesos 
        if len(self.ultimosAccesos) > 10:
            self.ultimosAccesos = self.ultimosAccesos[len(self.ultimos_accesos) - 10:]
                        
def insertar():
    # Creamos los productos
    # Estos se añaden correctamente
    prod1 = Producto(codigoBarras="5901234123457",nombre="pelota", catPrincipal=1, catSecundarias=[9,12])
    prod2 = Producto(codigoBarras="9780201379624",nombre="lapiz", catPrincipal=2)
    prod3 = Producto(codigoBarras="1234567891019",nombre="borrador", catPrincipal=3)
    prod4 = Producto(codigoBarras="1234567891026",nombre="cargador", catPrincipal=4)
    prod5 = Producto(codigoBarras="1234567891033",nombre="ordenador", catPrincipal=5)
    prod6 = Producto(codigoBarras="1234567891040",nombre="pantalla", catPrincipal=6)
    prod7 = Producto(codigoBarras="1234567891057",nombre="television", catPrincipal=7)
    prod8 = Producto(codigoBarras="1234567891064",nombre="teclado", catPrincipal=8)
    # Este debe fallar
    #prod9 = Producto(codigoBarras="5901234123453",nombre="holaaaa", catPrincipal=1, catSecundarias=[2,3])
    #prod9.save()
    prod1.save()
    prod2.save()
    prod3.save()
    prod4.save()
    prod5.save()
    prod6.save()
    prod7.save()
    prod8.save()
    #Creamos las tarjetas
    tarjeta1 = TarjetaCredito(nombreCompleto = "Pedro Sanchez",idTarjeta = "0965783091235449",mesCaducidad = 2,anioCaducidad = 2019,cvv = "347")
    tarjeta2 = TarjetaCredito(nombreCompleto = "Pedro Sanchez",idTarjeta = "3657404092176832",mesCaducidad = 9,anioCaducidad = 2018,cvv = "675")
    tarjeta3 = TarjetaCredito(nombreCompleto = "Pablo Iglesias",idTarjeta = "1234567891234567",mesCaducidad = 5,anioCaducidad = 2020,cvv = "123")
    tarjeta4 = TarjetaCredito(nombreCompleto = "Pablo Iglesias",idTarjeta = "9876543219876543",mesCaducidad = 4,anioCaducidad = 2019,cvv = "456")
    #creamos la linea de pedidos
    lineaDePedido_usuario1_1 = LineaDePedido(cantidadProductos = 2, precioProducto = 15.95, nombreProducto = "pelota", precioTotalLinea = 31.90,producto=prod1)
    lineaDePedido_usuario1_2 = LineaDePedido(cantidadProductos = 1, precioProducto = 4.00, nombreProducto = "lapiz", precioTotalLinea = 4.00,producto=prod2)
    lineaDePedido_usuario1_3 = LineaDePedido(cantidadProductos = 10, precioProducto = 30.00, nombreProducto = "borrador", precioTotalLinea = 300.00,producto=prod3)
    lineaDePedido_usuario1_4 = LineaDePedido(cantidadProductos = 1, precioProducto = 3.90, nombreProducto = "cargador", precioTotalLinea = 3.90,producto=prod4)
    lineaDePedido_usuario2_1 = LineaDePedido(cantidadProductos = 3, precioProducto = 1.00, nombreProducto = "ordenador", precioTotalLinea = 3.00,producto=prod5)
    lineaDePedido_usuario2_2 = LineaDePedido(cantidadProductos = 1, precioProducto = 0.00, nombreProducto = "pantalla", precioTotalLinea = 0.00,producto=prod6)
    lineaDePedido_usuario2_3 = LineaDePedido(cantidadProductos = 6, precioProducto = 2.00, nombreProducto = "television", precioTotalLinea = 12.00,producto=prod7)
    lineaDePedido_usuario2_4 = LineaDePedido(cantidadProductos = 2, precioProducto = 1.30, nombreProducto = "teclado", precioTotalLinea = 2.60,producto=prod8)
    #creamos los pedidos
    pedido_usuario1_1 = Pedido(precioTotalPedido = 35.90, fecha = "2017,12,01,17,32,45,111111", listaPedidos = [lineaDePedido_usuario1_1, lineaDePedido_usuario1_2])
    pedido_usuario1_2 = Pedido(precioTotalPedido = 303.90, fecha = "2017,12,02,17,32,45,111111", listaPedidos = [lineaDePedido_usuario1_3, lineaDePedido_usuario1_4])
    pedido_usuario2_1 = Pedido(precioTotalPedido = 3.00, fecha = "2017,12,03,17,32,45,111111", listaPedidos = [lineaDePedido_usuario2_1, lineaDePedido_usuario2_2])
    pedido_usuario2_2 = Pedido(precioTotalPedido = 14.60, fecha = "2017,12,04,17,32,45,111111", listaPedidos = [lineaDePedido_usuario2_3, lineaDePedido_usuario2_4])
   
    pedido_usuario1_1.save()
    pedido_usuario1_2.save()
    pedido_usuario2_1.save()
    pedido_usuario2_2.save()
    #creamos a los usuarios
    usuario1 = Usuario(dni = "51003098T",nombre = "Pedro",primerApellido = "Sanchez",fechaNacimiento = "1960-10-21",tarjetasCredito = [tarjeta1,tarjeta2],pedidos=[pedido_usuario1_1, pedido_usuario1_2])
    usuario2 = Usuario(dni = "12345678Z",nombre = "Pablo",primerApellido = "Iglesias",fechaNacimiento = "1980-02-01",tarjetasCredito = [tarjeta3,tarjeta4],pedidos=[pedido_usuario2_1, pedido_usuario2_2])

    usuario1.save()
    usuario2.save()
    
insertar()
