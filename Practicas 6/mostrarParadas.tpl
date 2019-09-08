<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<title>EMT</title>
<meta http-equiv="content-type" content="text/html" charset="utf-8" />
</head>
<body>
    <h1>Paradas cercanas a la calle {{listaMostrar[0]}} nº{{listaMostrar[1]}}</h1>
	
	% for i in range(2,len(listaMostrar)):
		%next = str(listaMostrar[i])
		%if "Parada" in next:
			</br></br>
		%end
		{{listaMostrar[i]}}
		%if i%2 == 0:
			</br>
		%end
	% end
	
	
	
	
	<a href="..">Volver a la página principal</a>
</body>
</html>