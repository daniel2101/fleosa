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
				<td width="20%">Cliente</td>
				<td width="15%">Producto</td>
				<td width="10%">Destino</td>
				<td width="10%">Día de Carga</td>
				<td width="15%">Cita con el Cliente</td>
				<td width="15%">Hora Real de Llegada</td>
				<td width="10%">Observaciones</td>
			</tr>
			<%
			    x = 1
			%>
			%for o in objects:
			<tr>
				<td>${o.unidad.name}</td>
				<td>${o.cliente.name}</td>
				<td>${o.producto.name}</td>
				<td>${o.name.partner_shipping_id.city}</td>
				<td>${o.fecha_salida_entrega}</td>
				<td>${o.name.fecha_entrega}</td>
				<td>${o.fecha_llega_entrega}</td>
				<td></td>

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
