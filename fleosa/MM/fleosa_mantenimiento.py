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
    
    
    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(('Acción Invalida !'), ('No es posible elimiar los registros, cancele la orden en el botón cancelar.'))
        return False
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'borrador',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'fleosa.mantenimiento.reparacion'),
            'fecha_solicitud': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_inicio': None,
            'fecha_fin': None,
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
        
    def button_iniciar(self, cr, uid, ids, context=None):
        orden_reparacion = self.browse(cr, uid, ids, context=context)[0]
        unidad = orden_reparacion.unidad
        contenedor = orden_reparacion.contenedor
        if not contenedor and not unidad:
            raise osv.except_osv("¡ERROR!", "Se debe seleccionar una unidad o un contenedor, al cual se le da mantenimiento.")
        if unidad.id:
            self.pool.get('fleosa.mu.unidades').write(cr, uid, [unidad.id], {'state': 'mantenimiento'})
        if contenedor.id:
            self.pool.get('fleosa.mu.contenedores').write(cr, uid, [contenedor.id], {'state': 'mantenimiento'})
        return self.write(cr, uid, ids, {'state': 'pendiente', 'fecha_inicio': datetime.today().strftime('%Y-%m-%d %H:%M:%S')})

    def button_terminar(self, cr, uid, ids, context=None):
        orden_reparacion = self.browse(cr, uid, ids, context=context)[0]
        unidad = orden_reparacion.unidad
        contenedor = orden_reparacion.contenedor
        if unidad.id:
            self.pool.get('fleosa.mu.unidades').write(cr, uid, [unidad.id], {'state': 'pension'})
        if contenedor.id:
            self.pool.get('fleosa.mu.contenedores').write(cr, uid, [contenedor.id], {'state': 'pension'})
        return self.write(cr, uid, ids, {'state': 'terminada', 'fecha_fin': datetime.today().strftime('%Y-%m-%d %H:%M:%S')})

    def button_cancelar(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancelada'})

    _columns = {
        'name': fields.char("Número de Orden de Reparación", size=24, required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'tipo': fields.selection((
            ('CORRECTIVO','CORRECTIVO'),
            ('PREVENTIVO', 'PREVENTIVO'),
        ), "Tipo de Mantenimiento", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'fecha_solicitud': fields.datetime("Fecha de Solicitud", required=True, readonly=True),
        'fecha_inicio': fields.datetime("Fecha de Inicio", readonly=True),
        'fecha_fin': fields.datetime("Fecha de Fin", readonly=True),
        'unidad': fields.many2one("fleosa.mu.unidades", "Unidad", help="Unidad a la que se le realiza la reparación", readonly=True, states={'borrador': [('readonly', False)]}),
        'contenedor': fields.many2one("fleosa.mu.contenedores", "Contenedor", help="Tanque al que se le realiza la reparación", readonly=True, states={'borrador': [('readonly', False)]}),
        'solicitud_uid': fields.many2one("hr.employee", "Solicitado por", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'state': fields.selection((
            ('borrador','Borrador'),
            ('pendiente', 'Pendiente'),
            ('terminada', 'Terminada'),
            ('cancelada', 'Cancelada'),
        ), "Estado"),
        # Material Utilizado en la reparación
        'material': fields.many2many("fleosa.mantenimiento.material", "fleosa_mantenimiento_reparacion_material", "reparacion_id", "material_id", "Material", states={'terminada': [('readonly', True)], 'cancelada': [('readonly', True)]}),
        'total_material': fields.function(_calcular_total, type="float", string="Total", store=True, readonly=True),
        'notas_material': fields.text("Notas", states={'terminada': [('readonly', True)], 'cancelada': [('readonly', True)]}),
        # Actividades de Mano de Obra
        'actividades': fields.many2many("fleosa.mantenimiento.actividades", "fleosa_mantenimiento_reparacion_actividades", "reparacion_id", "actividades_id", "Actividades", states={'terminada': [('readonly', True)], 'cancelada': [('readonly', True)]}),
        'total_horas': fields.function(_calcular_total_horas, type="float", string="Total de Horas", store=True, readonly=True),
        'notas_actividades': fields.text("Notas", states={'terminada': [('readonly', True)], 'cancelada': [('readonly', True)]}),
    }
    
    _order = 'name desc'
    
    _defaults = {
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fleosa.mantenimiento.reparacion'),
        'fecha_solicitud': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'borrador',
        'tipo': 'CORRECTIVO',
    }
        
fleosa_mantenimiento_reparacion()

class fleosa_mantenimiento_viaje(osv.osv):
    
    _name="fleosa.mantenimiento.viaje"
    
    _columns={
        'name': fields.many2one("res.partner","Cliente", required=True, help="Seleccione el cliente."),
        'producto': fields.many2one("product.product", "Producto", required=True),
        'origen': fields.char("Origen", size=200, required=True),
        'destino': fields.char("Destino", size=200, required=True)
    }

fleosa_mantenimiento_viaje()

class fleosa_mantenimiento_diesel(osv.osv):
    
    _name = "fleosa.mantenimiento.diesel"
    
    def on_change_unidad(self, cr, uid, ids, part):
        if not part:
            return {'value': {'operador': False, 'contenedor': False}}
        unidad = self.pool.get('fleosa.mu.unidades').browse(cr, uid, part)
        return {'value': {'operador': unidad.operador.id, 'contenedor': unidad.contenedor.id}}
    
    def unlink(self, cr, uid, ids, context=None):
        registros = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in registros:
            if s['state'] in ['borrador']:
                unlink_ids.append(s['id'])
            else: raise osv.except_osv(('Acción Invalida !'), ('Solo pueden ser eliminados los registros en borrador.'))
        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'borrador',
            'fecha': fields.date.context_today,
        })
        return super(fleosa_mantenimiento_reparacion, self).copy(cr, uid, id, default, context=context)
        
    
    def button_terminar(self, cr, uid, ids, context=None):
        registro = self.read(cr, uid, ids, context=context)[0]
        km_litro_cpu = registro['km_cpu']/ registro['litros_cpu']
        km_litro_real = registro['km_real']/ registro['litros_real']
        diferencia_litros = registro['litros_real'] - registro['litros_cpu']
        rendimiento = diferencia_litros/registro['litros_cpu']
        return self.write(cr, uid, ids, {'state': 'terminado', 'km_litro_cpu': km_litro_cpu, 'km_litro_real': km_litro_real, 'diferencia_litros': diferencia_litros, 'rendimiento': rendimiento*100})
        
    def on_change_calcular(self, cr, uid, ids, km_cpu, litros_cpu, km_real, litros_real):
        if litros_cpu == 0:
            litros_cpu = 1.0
        if litros_real == 0:
            litros_real = 1.0
        km_litro_cpu = float(km_cpu)/float(litros_cpu)
        km_litro_real = float(km_real)/float(litros_real)
        diferencia_litros = float(litros_real - litros_cpu)
        rendimiento = float(diferencia_litros/litros_cpu)
        return {'value': {'km_litro_cpu': km_litro_cpu, 'km_litro_real': km_litro_real, 'diferencia_litros': diferencia_litros, 'rendimiento': rendimiento*100}}
    
    _columns = {
        'name': fields.many2one("fleosa.mu.unidades", "Unidad", required=True, states={'terminado': [('readonly', True)]}),
        'contenedor': fields.many2one("fleosa.mu.contenedores", "Contenedor", states={'terminado': [('readonly', True)]}),
        'operador': fields.many2one("hr.employee", "Operador", required=True, states={'terminado': [('readonly', True)]}),
        'fecha': fields.date("Fecha", required=True, states={'terminado': [('readonly', True)]}),
        'peso': fields.float("Peso", digits=(4,1), states={'terminado': [('readonly', True)]}),
        'viajes': fields.many2many("fleosa.mantenimiento.viaje", "fleosa_mantenimiento_diesel_viaje", "diesel_id", "viaje_id", "Viajes", states={'terminado': [('readonly', True)]}),
        'km_cpu': fields.float("Kilometros CPU", digits=(6,1), states={'terminado': [('readonly', True)]}),
        'litros_cpu': fields.float("Litros CPU", digits=(6,1), states={'terminado': [('readonly', True)]}),
        'km_real': fields.float("Kilometros Real", digits=(6,1), states={'terminado': [('readonly', True)]}),
        'litros_real': fields.float("Litros Real", digits=(6,1), states={'terminado': [('readonly', True)]}),
        'km_litro_cpu': fields.float("Km/L CPU", digits=(4,3), readonly=True),
        'km_litro_real': fields.float("Km/L Real", digits=(4,3), readonly=True),
        'diferencia_litros': fields.float("Diferencia Litros", digits=(4,1), readonly=True), #litros real - litros cpu
        'rendimiento': fields.float("Rendimiento", digits=(4,3), readonly=True), # diferencia/litros_cpu
        'observaciones': fields.text("Observaciones"),
        'state': fields.selection((
            ('borrador', 'Borrador'),
            ('terminado', 'Terminado'),
        ), "Estado", required=True),
    }
    
    _order = 'id desc'
    
    _defaults = {
        'fecha': fields.date.context_today,
        'state': 'borrador',
    }
fleosa_mantenimiento_diesel()
