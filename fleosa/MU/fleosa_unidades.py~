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


from osv import osv, fields

class fleosa_mu_contenedores(osv.osv):
    _name = "fleosa.mu.contenedores"
    _columns = {
        'name': fields.char("Número Economico", size=20, required=True, help="Número que identifica el contenedor."),
        'placas': fields.char("Placas", size=10, required=True, help="Número de placas que tiene el contenedor."),
        'tipo': fields.selection((('30','30 Toneladas'),('35','35 Toneladas')), "Tamaño", help="Seleccione el tamaño del tanque."),
        'state': fields.selection([('pension','En pensión'),
            ('descompuesta','Descompuesta'),
            ('mantenimiento','En mantenimiento'),
            ('viaje','En viaje'),
            ('desuso','Desuso')], "Estado", required=True, help="Estado en el que se encuentra la unidad."),
        'anotaciones': fields.text("Anotaciones"),
    }
    
    _defaults = {
        'state': "pension",
        'tipo': '30',
    }
fleosa_mu_contenedores()

class fleosa_mu_unidades(osv.osv):
    _name = "fleosa.mu.unidades"
    _columns = {
        'name': fields.char("Número Economico", size=20, required=True, help="Número que identifica la unidad."),
        'dueno': fields.many2one("hr.employee","Dueño", required=True, help="Dueño de la unidad."),
        'placas': fields.char("Placas", size=10, required=True, help="Número de placas que tiene la unidad."),
        'operador': fields.many2one("hr.employee", "Operador", help="Si la unidad tiene asignado un operador seleccionelo."),
        'contenedor': fields.many2one("fleosa.mu.contenedores", "Tanque", help="Si la unidad cuenta con un tanque asignado seleccionelo."),
        'state': fields.selection([('pension','En pensión'),
            ('descompuesta','Descompuesta'),
            ('mantenimiento','En mantenimiento'),
            ('viaje','En viaje'),
            ('desuso','Desuso')], "Estado", required=True, help="Estado en el que se encuentra la unidad."),
        'anotaciones': fields.text("Anotaciones"),
    }
    _defaults = {
        'state': "pension",
    }
fleosa_mu_unidades()
