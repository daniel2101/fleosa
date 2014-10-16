# -*- coding: utf-8 -*-
##############################################################################
#
#    Desarrollado por rNet Soluciones
#    Jefe de Proyecto: Ing. Ulises Tlatoani Vidal Rieder
#    Desarrollador: Ing. Salvador Daniel Pelayo Gómez.
#    Analista: Lic. David Padilla Bobadilla
#
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# Manejo de versiones:
# Primer digito es la versión del release (entrega a fleosa).
# El segundo digito es la versión de actualización (funcional a nivel de instalación)
# El tercer digito es el número de modidificación de algún script, consecutivo para todo el desarrollo

{
    "name" : "Fleosa",
    "version" : "2.35.112",
    "depends": ["base", "l10n_mx_states", "cfdi_rnet", "purchase", "hr"],
    "author" : "Salvador Daniel Pelayo Gómez, Ulises Vidal Rieder, David Padilla Bobadilla, Luis Miguel",
    "website": "http://rnet.mx",
    "category" : "Generic Modules/Others",
    "description" : """
Modulo para Fleosa:
        Manejo de Unidades, Operadores, Mantnimiento, Logistica, Ventas, Compras, Facturación. 
        1) MO Operadores.
        2) MU Unidades.
        3) ML Logistica.
        4) MV Ventas.
        5) MC Compras. Posiblemente no se necesita modificar codigo.
        6) MF Facturación. Posiblemente no se necesita modificar codigo.
        7) MM Mantenimiento.
        8) MP Producto.
        9) MTP Registo de tiempos y pesos.
""",
    "init_xml" : [],
    "update_xml" : ["fleosa_view.xml",
                    "MO/view.xml",
                    "MU/view.xml",
                    "ML/view.xml",
                    "MV/view.xml",
                    "MP/view.xml",
                    "MTP/view.xml",
                    "MTP/ORIGINALview.xml",
                    "MM/sequence.xml",
                    "MM/view.xml",
                    "report/report.xml",
                    "security/fleosa_security.xml",
                    "security/ir.model.access.csv"],
    "demo_xml" : [],
    "installable" : True,
    'auto_install': True,
    'application': True,
}
