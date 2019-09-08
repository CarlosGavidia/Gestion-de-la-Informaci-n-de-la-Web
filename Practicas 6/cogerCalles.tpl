<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<title>EMT</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
</head>
<body>
	<h1>Ruta más óptima: </h1>
    <h2>Rellena los campos</h2>
	<form action="/cogerCalles" method="post">
        Calle Origen: <input name="calleOrigen" type="text" required/>
        NºCalle Origen: <input name="ncalleOrigen" type="number" required/>
		Calle Destino: <input name="calleDestino" type="text" required />
		NªCalle Destino: <input name="ncalleDestino" type="number" required/>
        <input value="Enviar" type="submit" />
    </form>
	<a href="..">Volver a la página principal</a>
</body>
</html>