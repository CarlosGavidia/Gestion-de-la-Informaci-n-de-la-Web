<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<title>EMT</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
</head>
<body>
    <h1>Descripcion de la ruta desde la calle {{listaMostrar[0]}} nº{{listaMostrar[1]}} hasta la calle {{listaMostrar[2]}} nº{{listaMostrar[3]}}</h1>
	<h4>Fecha de la ruta: {{listaMostrar[4]}}</h4>
	<h4>Hora de inicio de la ruta: {{listaMostrar[5]}}</h4>
	<h4>Hora estimada de llegada: {{listaMostrar[6]}}</h4>
	<h4>Número de trasbordos: {{listaMostrar[7]}}</h4>
	<h4>Duración del viaje: {{listaMostrar[8]}}</h4>
	<h4>Descripcion textual de la ruta:</h4>
	<ul>
		% for i in range(9,len(listaMostrar)):
			<li> {{listaMostrar[i]}} </li>
		% end
	</ul>
	<a href="..">Volver a la página principal</a>
</body>
</html>