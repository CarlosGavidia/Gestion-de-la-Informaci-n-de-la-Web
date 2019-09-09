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
<title>Usuarios</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body>
    <h2>Número de usuarios encontrados:{{consulta.count()}}</h4>
	% if consulta.count() > 0:
		<table>
		  <tr>
			<th>Nombre de usuario</th>
			<th>e-mail</th> 
			<th>Página web</th>
			<th>Tarjeta de crédito</th>
			<th>Hash de contrase˜nia</th>
			<th>Nombre</th>
			<th>Apellido</th>
			<th>Dirección</th>
			<th>Aficiones</th>
			<th>Fecha de nacimiento</th>
		  </tr>
		  <tr>
			% for fila in consulta:
				<td>{{fila['_id']}}</td>
				<td>{{fila['email']}}</td>
				<td>{{fila['webpage']}}</td>
				<td>{{fila['credit_card']['number']}}Caducidad:{{fila['credit_card']['expire']['month']}}/{{fila['credit_card']['expire']['year']}}</td>
				<td>{{fila['password']}}</td>
				<td>{{fila['name']}}</td>
				<td>{{fila['surname']}}</td>
				<td>C/:{{fila['address']['street']}} Nº{{fila['address']['num']}},{{fila['address']['country']}},COD:{{fila['address']['zip']}}</td>
				<td>
					<ul>
					%for gusto in fila['likes']:
					  <li>{{gusto}}</li>
					%end
					</ul>
				</td>
				<td>{{fila['birthdate']}}</td>
			</tr>
			%end
		</table>
	
</body>
</html>