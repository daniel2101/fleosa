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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from osv import osv, fields

class fleosa_mantenimiento_material(osv.osv):
    _name = 'fleosa.mantenimiento.material'
    
    def on_change_producto(self, cr, uid, ids, producto_id, cantidad):
        if not producto_id:
            return {'value':{}}
        producto = self.pool.get('product.product').browse(cr, uid, [producto_id], context=None)[0]
        subtotal = cantidad * producto.standard_price
        vals = {'value' : {'descripcion': producto.name, 'unidad': producto.uom_id.id, 'precio_unidad': producto.standard_price, 'subtotal': subtotal}}
        return vals
        
        
    def on_change_cantidad  (self, cr, uid, ids, cantidad, precio):
        if not cantidad or not precio:
            return {'value':{'subtotal': 0.0}}
        subtotal = cantidad * precio
        return {'value' : {'subtotal': subtotal}}
        
                    
    _columns = {
        'name': fields.many2one("product.product", "Producto", required=True),
        'descripcion': fields.char("Descripción", size=500, required=True),
        'cantidad': fields.float("Cantidad", required=True, digits=(6,2)),
        'unidad': fields.many2one("product.uom", "UDM", required=True),
        'precio_unidad': fields.float("Precio", required=True, digits=(8,2)),
        'subtotal': fields.float("SubTotal", required=True, digits=(8,2)),
    }
    
    _defaults = {
        'cantidad': 1,
    }
    
fleosa_mantenimiento_material()

class fleosa_mantenimiento_actividades(osv.osv):
    _name = 'fleosa.mantenimiento.actividades'
    _columns = {
        'name': fields.char("Actividad", size=150, required=True, help="Actividad de mantenimiento realizada."),
        'descripcion': fields.char("Descripción", size=500, required=True, help="Descripción de lo que se realizó."),
        'empleado': fields.many2one("hr.employee", "Empleado", required=True),
        'duracion': fields.float("Duración", required=True, digits=(4,1), help="Tiempo en horas que se le dedico a dicha actividad. Ej: 3.5"),
    }
    
    _defaults = {
        'duracion': 1.0,
    }
    
fleosa_mantenimiento_actividades()

class fleosa_mantenimiento_reparacion(osv.osv):

    _name = 'fleosa.mantenimiento.reparacion'
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'borrador',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'fleosa.mantenimiento.reparacion'),
            'fecha_solicitud': fields.date.context_today,
        })
        return super(fleosa_mantenimiento_reparacion, self).copy(cr, uid, id, default, context=context)
    
    def _calcular_total(self, cr, uid, ids, name, arg, context=None):
        record_id=ids[0]
        total = 0.0
        orden_reparacion = self.browse(cr, uid, ids, context=context)[0]
        for material in orden_reparacion.material:
            total = total + material.subtotal
        return {record_id: total}
        
    def _calcular_total_horas(self, cr, uid, ids, name, arg, context=None):
        record_id=ids[0]
        total = 0.0
        orden_reparacion = self.browse(cr, uid, ids, context=context)[0]
        for actividad in orden_reparacion.actividades:
            total = total + actividad.duracion
        return {record_id: total}

    _columns = {
        'name': fields.char("Número de Orden de Reparación", size=24, required=True),
        'tipo': fields.selection((
            ('CORRECTIVO','CORRECTIVO'),
            ('PREVENTIVO', 'PREVENTIVO'),
        ), "Tipo de Mantenimiento", required=True),
        'fecha_solicitud': fields.datetime("Fecha de Solicitud", required=True),
        'fecha_inicio': fields.datetime("Fecha de Inicio"),
        'fecha_fin': fields.datetime("Fecha de Fin"),
        'unidad': fields.many2one("fleosa.mu.unidades", "Unidad", help="Unidad a la que se le realiza la reparación"),
        'contenedor': fields.many2one("fleosa.mu.contenedores", "Contenedor", help="Tanque al que se le realiza la reparación"),
        'solicitud_uid': fields.many2one("hr.employee", "Solicitado por", required=True),
        'state': fields.selection((
            ('borrador','Pendiente'),
            ('terminada', 'Terminada'),
            ('cancelada', 'Cancelada'),
        ), "Estado"),
        # Material Utilizado en la reparación
        'material': fields.many2many("fleosa.mantenimiento.material", "fleosa_mantenimiento_reparacion_material", "reparacion_id", "material_id", "Material"),
        'total_material': fields.function(_calcular_total, type="float", string="Total", store=True, readonly=True),
        'notas_material': fields.text("Notas"),
        # Actividades de Mano de Obra
        'actividades': fields.many2many("fleosa.mantenimiento.actividades", "fleosa_mantenimiento_reparacion_actividades", "reparacion_id", "actividades_id", "Actividades"),
        'total_horas': fields.function(_calcular_total_horas, type="float", string="Total de Horas", store=True, readonly=True),
        'notas_actividades': fields.text("Notas"),
    }
    
    _defaults = {
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fleosa.mantenimiento.reparacion'),
        'fecha_solicitud': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'borrador',
        'tipo': 'CORRECTIVO',
    }

fleosa_mantenimiento_reparacion()


class fleosa_mantenimiento_diesel(osv.osv):
    
    _name = "fleosa.mantenimiento.diesel"
    
    _columns = {
        'name': fields.many2one("fleosa.mu.unidades", "Unidad", required=True),
        'contenedor': fields.many2one("fleosa.mu.contenedores", "Contenedor"),
        'carta_porte_id': fields.many2one("fleosa.ml.cp", "Carta Porte", readonly=True),
        'operador': fields.many2one("hr.employee", "Operador", required=True),
        'fecha': fields.date("Fecha"),
        'peso': fields.integer("Peso"),
        'km_cpu': fields.integer("Kilometros CPU"),
        'litros_cpu': fields.integer("Litros CPU"),
        'km_real': fields.integer("Kilometros Real"),
        'litros_real': fields.integer("Litros Real"),
        'km_litro_cpu': fields.integer("Km/L CPU"),
        'km_litro_real': fields.integer("Km/L Real"),
        'diferencia_litros': fields.integer("Diferencia Litros"), #litros real - litros cpu
        'rendimiento': fields.integer("Rendimiento"), # diferencia/litros_cpu
        'observaciones': fields.text("Observaciones"),
    }
    
fleosa_mantenimiento_diesel()
