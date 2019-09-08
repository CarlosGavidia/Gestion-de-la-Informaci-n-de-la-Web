<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<title>EMT</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
</head>
<body>
    <h1>Puntos de interés desde la calle {{listaMostrar[0]}} nº{{listaMostrar[1]}} hasta la calle {{listaMostrar[2]}} nº{{listaMostrar[3]}}</h1>
	<ul>
		% for i in range(4,len(listaMostrar)-4,4):
			<h3> {{listaMostrar[i]}} </h3>
			<li> Calle {{listaMostrar[i+1]}} Nº {{listaMostrar[i+2]}} </li>
			<li> Teléfono: {{listaMostrar[i+3]}} </li>
		% end
	</ul>
	<a href="..">Volver a la página principal</a>
</body>
</html>