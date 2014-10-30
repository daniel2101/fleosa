<html>
<head>
     <style type="text/css">
                ${css}
            </style>
</head>
<body>
    %for o in objects:
    <% setLang(o.partner_id.lang) %>

	      
		<table  width="100%" class="subtitle">
                <tr>
                    <td style="font-size:120%">
                        <b> ${ _('Carta Porte No.') } ${o.name}</b>
                    </td>
                </tr>
                <tr>
                    <td style="text-align:right">
            			<b> ${ _('Lugar y Fecha de Expedición: ') }${ _('Morelia Michoacán a ') } ${o.date_order}</b>
                    </td>
                </tr>
            	</table><br/>		
		<table class="basic_table" width="100%">
			<tr>
				<td width="10%" align="left">
					Origen:
				</td>
				<td width="40%" align="center">
					<b>${format(o.carta_porte_id.origen)}</b>
				</td>
				<td width="10%" align="left">
					Destino:
				</td>
				<td width="40%" align="center">
					<b>${format(o.partner_shipping_id.city)}, ${format(o.partner_shipping_id.state_id.name)}.</b>
				</td>
			</tr>
			<tr>
				<td width="10%" align="left">
					Remitente:
				</td>
				<td width="40%">
					<b>${format(o.partner_id.name)}</b>
				</td>
				<td width="10%" align="left">
					Destinatario:
				</td>
				<td width="40%">
					<b>${format(o.partner_destinatario_id.name)}</b>
				</td>
			</tr>
			<tr>
				<td width="10%" align="left">
					RFC:
				</td>
				<td width="40%">
					<b>${format(o.partner_id.vat)}</b>
				</td>
				<td width="10%" align="left">
					RFC:
				</td>
				<td width="40%">
					<b>${format(o.partner_destinatario_id.vat)}</b>
				</td>
			</tr>
			<tr>
				<td width="10" align="left">
					Dirección:
				</td>
				<td width="40%">
					<b>${format(o.partner_direccion_remitente.street)} No. ${format(o.partner_direccion_remitente.street3)}. Col. ${format(o.partner_direccion_remitente.street2)}</b>
				</td>
				<td width="10%" align="left">
					Dirección:
				</td>
				<td width="40%">
					<b>${format(o.partner_shipping_id.street)} No. ${format(o.partner_shipping_id.street3)}. Col. ${format(o.partner_shipping_id.street2)}</b>
				</td>
			</tr>
			<tr>
				<td width="10%" align="left">
					Fecha Embarque:
				</td>
				<td width="40%">
					<b>${format(o.carta_porte_id.fecha_embarque)}</b>
				</td>
				<td width="10%" align="left">
					Fecha Entrega:
				</td>
				<td width="40%">
					<b>${format(o.carta_porte_id.fecha_entrega)}</b>
				</td>
			</tr>
		</table></br>
		<table width="100%" class="basic_table">
			<tr>
				<td width="34%" style="font-size:8;text-align:left">
					Valor Unitario, Cuota Convenida</br>
					Por Tonelada o Carga Fraccionada
					<b style="font-size:10">${o.order_line[0].price_unit}</b>
				</td>
				<td width="33%" style="font-size:8;text-align:left">
					Valor</br>
					Declarado
					<b style="font-size:10">${o.carta_porte_id.valor_declarado}</b>		
				</td>
				<td width="33%" style="font-size:8;text-align:left">
					Condiciones</br>
					De Pago				
				</td>
		</table>


		<table  width="100%">
                <tr>
                    <td style="font-size:10"><br/>
                        <b> ${ _('EL QUE REMITE DICE QUE CONTIENE:') }</b><br/>
                    </td>
                </tr>
		</table>
		<table class="basic_table" width="100%">
			<tr>
				<td width="10%">
					<b>${_("Número")}</b>
				</td>
				<td width="10%">
					<b>${_("Embalaje")}</b>
				</td>
				<td width="40%">
					<b>${_("Contenido")}</b>
				</td>
				<td width="15%">
					<b>${_("Peso Real")}</b>
				</td>
				<td width="10%">
					<b>${_("Volumen")}</b>
				</td>
				<td width="15%">
					<b>${_("Peso Estimado")}</b>
				</td>
			</tr>
			<tr>
				<td width="10%">					
				</td>
				<td width="10%">
				</td>
				<td width="40%" align="left">
					<p>Tons. Neto de: <b>${format(o.carta_porte_id.producto_transportar.name)}</b></p>
					% if o.carta_porte_id.sellos:
                        <p>Sellos: <b>${o.carta_porte_id.sellos}</b></p>
                    % else:
                        <p>Sellos:</p>
                    % endif
                    % if o.carta_porte_id.remision:
                        <p>Remisión: <b>${o.carta_porte_id.remision}</b></p>
                    % elif o.client_order_ref:
                        <p>Remisión: <b>${o.client_order_ref}</b></p>
                    % else:
                        </br>
                    % endif
					<p>ANEXO CERTIFICADO DE CALIDAD</p>
				</td>
				<td width="15%">
                    % if o.pesos_tiempos_id.peso_neto_o:
                        <p>Sellos: <b>${o.pesos_tiempos_id.peso_neto_o}</b></p>
                    % else:
                        <br/>
                    % endif
				</td>
				<td width="10%">
				</td>
				<td width="15%">
                    <p><b>${o.carta_porte_id.cantidad}</b></p>
				</td>
			</tr>
		</table></br>
		<table class="list_table" width="100%">
			<tr>
				<td width="30%">
					<b>${_("Concepto")}</b>
				</td>
				<td width="10%">
					<b>${_("Impuesto")}</b>
				</td>
				<td width="20%" style="text-align:right">
					<b>${_("Cantidad")}</b>
				</td>
				<td width="20%" align="right" style="text-align:right">
					<b>${_("Precio Unitario")}</b>
				</td>
				<td width="20%" style="text-align:right">
					<b>${_("Importe")}</b>
				</td>
			</tr>
		</table>
		%for line in o.order_line:
			<table class="concept_table" width="100%">
    		<tr>
    			<td width="30%"> 
    				${ format(line.name) }
    			</td>
    			<td width="10%">
    				${ ', '.join(map(lambda x: x.name, line.tax_id)) }
    			</td>
    			<td width="20%" style="text-align:right">
    				${ formatLang(line.product_uos and line.product_uos_qty or line.product_uom_qty) } ${ line.product_uos and line.product_uos.name or line.product_uom.name }
    			</td>
    			<td width="20%" style="text-align:right">
    				${ formatLang(line.price_unit , digits=get_digits(dp='Product Price')) }
    			</td>
    			
    			<td width="20%" style="text-align:right">
    				${ formatLang(line.price_subtotal, digits=get_digits(dp='Account'), currency_obj=o.pricelist_id.currency_id) }
    			</td>
			
    		</tr>
    	</table>
		%endfor

	<table width="100%">
    		<tr>
    			<td width="70%">
    			</td>
    			<td width="30%" style="border-top: 1px solid #000000; text-align:left">
    				<table width="100%" class="tr_top" style="font-size:12">
			    		<tr>
			    			<td style="text-align:left">
			    				${_("Total Neto:")}
			    			</td>
			    			<td style="text-align:right">
			    				${ formatLang(o.amount_untaxed, dp='Account', currency_obj=o.pricelist_id.currency_id) }
			    			</td>
			    		</tr>
			    		<tr>
			    			<td >
			    				${_("IVA 16%:")}
			    			</td>
			    			<td style="text-align:right"> 
			    				${ formatLang(o.amount_untaxed*0.16, dp='Account', currency_obj=o.pricelist_id.currency_id) }
			    			</td>
			    		</tr>
					<tr>
			    			<td style="text-align:left">
			    				${_("Sub Total:")}
			    			</td>
			    			<td style="text-align:right">
			    				${ formatLang(o.amount_untaxed*1.16, dp='Account', currency_obj=o.pricelist_id.currency_id) }
			    			</td>
			    		</tr>
			    		<tr>
			    			<td >
			    				${_("Retención IVA:")}
			    			</td>
			    			<td style="text-align:right"> 
			    				${ formatLang(o.amount_untaxed*1.16-o.amount_total, dp='Account', currency_obj=o.pricelist_id.currency_id) }
			    			</td>
			    		</tr>
					
			    	</table>
    			</td>
    		</tr>
    		<tr>
    			<td></td>
    			<td style="border-top: 1px solid #000000; text-align:left">
    				<table width="100%" class="tr_top" style="font-size:12">
    					<tr>
    						<td>
    							<b>${_("Total :")}</b>
				    		</td>
				    		<td align="right">
				    			<b>${ formatLang(o.amount_total, dp='Account', currency_obj=o.pricelist_id.currency_id) }</b>
				    		</td>
				 		</tr>
				 	</table>
				 </td>
			</tr>	
    	</table>

	</br>
	<table class="list_table" width="100%">
		<tr>
			<td width="20%">
			Operador:
			</td>
			<td width="30%">
			${ format(o.carta_porte_id.operador.name)}
			</td>
			<td width="20%">
			Licencia:
			</td>
			<td width="30%">
			${ format(o.carta_porte_id.operador.identification_id)}
			</td>
		</tr>
		<tr>
			<td width="20%">
			Placas</br>
			Camion:
			</td>
			<td width="30%">
			${ format(o.carta_porte_id.unidad.placas)}
			</td>
			<td width="20%">
			Placas</br>
			Contenedor:
			</td>
			<td width="30%">
			${ format(o.carta_porte_id.contenedor.placas)}
			</td>
		</tr>
		<tr>
			<td width="20%">
			Observaciones:
			</td>
			<td width="30%">
			
			</td>
			<td width="20%">
			Documento:
			</td>
			<td width="30%">
			</td>
		</tr>
	
	</table>	
	</br></br></br>

    <table  width="60%" class="subtitle" align="center">
        <tr>
            <td style="font-size:10">
                <b> ${ _('Recibí de Conformidad:') }</b>
            </td>
            <td width="70%" style="border-bottom: 1px solid #000000; text-align:left">
            </td>
        </tr>
        <tr>
            <td></td>
            <td style="font-size:8;text-align:center">
                Firma del Destinatario
            </td>
        </tr>
    </table>
	</br>

	<p style="page-break-after:always"></p>
	
		%if o.carta_porte_id.multi_direcciones:
            </br>
			<table class="subtitle" width="100%">
				<tr>
					<td width="50%"><b>LUGARES DE ENTREGA ADICIONALES</b></td>
				</tr>
				<tr>
					<td width="50%">SE RECOGERÁ EN: </td>
					<td>SE ENTREGARÁ EN: </td>
				</tr>
			%for d in o.carta_porte_id.multi_direcciones:
				<tr>
					<td width="50%"><div style="color:#000000">
  						<h3>${ d.name.city },${ d.name.state_id.name }</h3>
  						<p>Calle: ${ d.name.street }</p>
                        <p>No. ${ d.name.street3 }</p>
						<p>Colonia: ${ d.name.street2 }</p>
                        <p>Código Postal: ${ d.name.zip }</p>
					</div></td>
					<td><div style="color:#000000">
  						<h3>${ d.destino.city },${ d.destino.state_id.name }</h3>
  						<p>Calle: ${ d.destino.street }</p>
                        <p>No. ${ d.destino.street3 }</p>
						<p>Colonia: ${ d.destino.street2 }</p>
                        <p>Código Postal: ${ d.destino.zip }</p>
					</div></td>
				</tr>
			%endfor
			</table>
		
		%endif
    	%endfor
</body>
</html>
