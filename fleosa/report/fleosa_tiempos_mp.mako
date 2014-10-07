<html>
	<head>
		<style type="text/css">
			${css}
		</style>
	</head>
	<body>
		<table  width="100%" class="resumen">
			<tr>
				<td width="5%">No. Económico</td>
				<td width="10%">Placas Tra</td>
				<td width="20%">Nombre del Operador</td>
				<td width="5%">Tanque</td>
				<td width="10%">Placas Tanque</td>
				<td width="10%">Proveedor</td>
				<td width="15%">Producto</td>
				<td width="15%">Origen</td>
				<td width="10%">Llegada Estimada</td>
			</tr>
			<%
			    x = 1
			%>
			%for o in objects:
			<tr>
				<td>${o.name.unidad.name}</td>
				<td>${o.name.unidad.placas}</td>
				<td>${o.name.operador.name}</td>
				<td>${o.name.contenedor.name}</td>
				<td>${o.name.contenedor.placas}</td>
				<td>${o.name.partner_id.name}</td>
				<td>${o.name.producto_transportar.name}</td>
				<td>${o.name.partner_invoice_id.city}</td>
				<td>${o.name.fecha_entrega}</td>

			</tr>
			<%
				x = x + 1
			%>

			%endfor
		</table>
		<br/>
		<p style="page-break-after:always"></p>
	</body>
</html>
