<html>
	<head>
		<style type="text/css">
			${css}
		</style>
	</head>
	<body>
		<table  width="100%" class="resumen">
			<tr>
				<td width="5%">No. de Viaje</td>
				<td width="5%">Placas</td>
				<td width="10%">Operador</td>
				<td width="5%">Fecha</td>
				<td width="10%">Cliente</td>
				<td width="10%">Ciudad Destino</td>
				<td width="10%">Producto</td>
				<td width="5%">Remisión AAK</td>
				<td width="5%">C.P.</td>
				<td width="5%">Precio</td>
				<td width="5%">Maniobras</td>
				<td width="5%">Reparto</td>
				<td width="5%">Báscula</td>
				<td width="5%">Estancia</td>
				<td width="5%">Cantidad Cargada</td>
				<td width="5%">Cantidad Recibida</td>
			</tr>
			<%
			    x = 1
			%>
			%for o in objects:
			<% setLang(o.partner_id.lang) %>
			<tr>
				<td>${x}</td>
				<td>${o.carta_porte_id.unidad.placas}</td>
				<td>${o.carta_porte_id.operador.name}</td>
				<td>${o.carta_porte_id.fecha_entrega}</td>
				<td>${o.partner_destinatario_id.name}</td>
				<td>${o.carta_porte_id.destino}</td>
				<td>${o.carta_porte_id.producto_transportar.name}</td>
				% if o.carta_porte_id.remision:
                    <td>${o.carta_porte_id.remision}</td>
                % elif o.client_order_ref:
                    <td>${o.client_order_ref}</td>
                % else:
                    <td>-</td>
                % endif
				<td>${o.name}</td>
				%for line in o.order_line:
					<td>${line.price_subtotal}</td>
				%endfor
				<td>${o.pesos_id.peso_bruto_o - o.pesos_id.peso_tara_o}</td>
				<td>${o.pesos_id.peso_bruto_d - o.pesos_id.peso_tara_d}</td>
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
