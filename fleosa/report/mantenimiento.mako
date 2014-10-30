<html>
	<head>
		<style type="text/css">
			${css}
		</style>
	</head>
	<body>
        %for o in objects:
            <table  width="100%" class="subtitle">
                <tr>
                    <td style="font-size:120%">
                        <b> ${ _('Orden de Reparación No.') } ${o.name}</b>
                    </td>
                </tr>
            </table><br/>

            <table class="list_table" width="100%">
                <tr>
                    <td width="15%"><b>Tipo de Servicio</b></td>
                    <td width="35%">${o.tipo}</td>
                    <td width="15%"><b>Solicita</b></td>
                    <td width="35%">${o.solicitud_uid.name}</td>
                </tr>
                <tr>
                    %if o.unidad:
                        %if o.contenedor:
                            <td width="15%"><b>Unidad</b></td>
                            <td width="35%">${o.unidad.name}</td>
                            <td width="15%"><b>Contenedor</b></td>
                            <td width="35%">${o.contenedor.name}</td>
                        %else:
                        <td colspan="2"><b>Unidad</b></td>
                        <td colspan="2">${o.unidad.name}</td>
                        %endif
                    %elif o.contenedor:
                        <td colspan="2"><b>Contenedor</b></td>
                        <td colspan="2">${o.contenedor.name}</td>
                    %endif
                </tr>
                <tr>
                    <td width="15%"><b>Fecha de Inicio</b></td>
                    <td width="35%">${o.fecha_inicio}</td>
                    <td width="15%"><b>Fecha de Fin</b></td>
                    <td width="35%">${o.fecha_fin}</td>
                </tr>
            </table>
            <br/>

            <div class="enc">
                <h2>Actividades</h2>
                <table class="list_table" width="100%">
                    <tr>
                        <td width="20%">Actividad</td>
                        <td width="40%">Descripción</td>
                        <td width="25%">Empleado</td>
                        <td width="15%" style="text-align:right">Duración</td>
                    </tr>
                </table>
                <%
                    x=1
                %>
                %for act in o.actividades:
   		    	    <table class="concept_table" width="100%">
               	    	<tr>
               	    		<td width="20%" style="text-align:left"> 
               	    			${x}. ${act.name}
               	    		</td>
               	    		<td width="40%" style="text-align:left">
               	    			${act.descripcion}
               	    		</td>
               	    		<td width="25%" style="text-align:left">
               	    			${act.empleado.name}
               	    		</td>
               	    		<td width="15%" style="text-align:right">
               	    			${act.duracion} hrs.
               	    		</td>
                   		</tr>
                   	</table>
                <%
				    x = x + 1
			    %>
      	    	%endfor
                <table width="100%">
                    <tr>
                       	<td width="70%"></td>
                   		<td width="30%" style="border-top: 1px solid #000000; text-align:left">
                   			<table width="100%" class="tr_top" style="font-size:12">
               			   		<tr>
       						        <td><b>Duración Total :</b></td>
   				    		        <td align="right"><b>${o.total_horas} hrs</b></td>
   				 		        </tr>
   				 	        </table>
   				        </td>
   			        </tr>	
       	        </table>
            </div>
            <br/>

            %if o.material:
                <div class="enc">             
                    <h2>Material</h2>      		
                    <table class="list_table" width="100%">
        	    		<tr>
        	    			<td width="20%">
        	    				<b>Producto</b>
        	    			</td>
        	    			<td width="30%">
        	    				<b>Descripción</b>
        	    			</td>
        	    			<td width="10%" style="text-align:right">
        	    				<b>Cantidad</b>
        	    			</td>
        	    			<td width="20%" align="right" style="text-align:right">
        	    				<b>Precio Unitario</b>
        	    			</td>
        	    			<td width="20%" style="text-align:right">
        	    				<b>Importe</b>
        	    			</td>
        	    		</tr>
        	    	</table>
                    %for mat in o.material:
    		    	    <table class="concept_table" width="100%">
                	    	<tr>
                	    		<td width="20%" style="text-align:left"> 
                	    			${mat.name.name}
                	    		</td>
                	    		<td width="30%" style="text-align:left">
                	    			${mat.descripcion}
                	    		</td>
                	    		<td width="10%" style="text-align:right">
                	    			${mat.cantidad}
                	    		</td>
                	    		<td width="20%" style="text-align:right">
                	    			$ ${mat.precio_unidad}
                	    		</td>
    			    
                	    		<td width="20%" style="text-align:right">
                 				    $ ${mat.subtotal}
                    			</td>
			    
                    		</tr>
                    	</table>
        	    	%endfor
                    <table width="100%">
                        <tr>
                         	<td width="70%"></td>
                     		<td width="30%" style="border-top: 1px solid #000000; text-align:left">
                    			<table width="100%" class="tr_top" style="font-size:12">
                			   		<tr>
        						        <td><b>Total :</b></td>
    				    		        <td align="right"><b>$ ${o.total_material}</b></td>
    				 		        </tr>
    				 	        </table>
    				        </td>
    			        </tr>	
        	        </table>
                </div>
            %endif	


		    <br/>
		    <p style="page-break-after:always"></p>
        %endfor
	</body>
</html>
