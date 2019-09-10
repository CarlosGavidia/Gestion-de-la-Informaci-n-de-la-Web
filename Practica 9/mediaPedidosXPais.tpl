<!--# -*- coding: utf-8 -*-
 
##
#Carlos Gavidia Ortiz,Iván Monterrubio Cerezo,Sergio González Jiménez y José Antonio Bernal Pérez declaramos que esta solución
#es fruto exclusivamente nuestro trabajo personal. No hemos sido
#ayudados por ninguna otra persona ni hemos obtenido la solución de
#fuentes externas, y tampoco hemos compartido nuestra solución con
#nadie. Declaramos además que no hemos realizado de manera deshonesta
#ninguna otra actividad que pueda mejorar nuestros resultados
#ni perjudicar los resultados de los demás.
##-->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<title>Promedio de líneas de pedidos por países</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
</head>
<body>
		<table>
		  <tr>
			<th>País</th>
			<th>Media de pedidos</th> 
		  </tr>
		  <tr>
			%contador=0
			% for fila in consulta:
			%contador=contador+1
				<td>{{fila['_id']}}</td>
				<td>{{fila['lineasPromedio']}}</td>
			</tr>
			%end
		</table>
	<h2>Número de resultados encontrados:{{contador}}</h2>
</body>
</html>