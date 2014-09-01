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

class fleosa_config(osv.osv):

    def activar(self, cr, uid, ids, context=None):
        config_ids = self.search(cr, uid, [])
        for i in config_ids:
            self.write(cr, uid, i, {'activo': False})
        return self.write(cr, uid, ids, {'activo':True})

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv("ERROR!", "No es posible eliminar el registro de configuración!")
        return False

    def copy(self, cr, uid, id, default=None, context=None):
        raise osv.except_osv("ERROR!", "No es posible realizar copia del registro de configuración!")
        return False
    
    def write(self, cr, uid, ids, vals, context=None):
        vals['user_id'] = uid
        return super(fleosa_config, self).write(cr, uid, ids, vals, context=context)

    _name = "fleosa.config"
    _columns = {
        'name': fields.char("Nombre de configuración", size=64, required=True),
        'user_id': fields.many2one("res.users", "Usuario", readonly=True),
        'activo': fields.boolean("Activo"),
        #Datos de configuración para ventas
        #TODO Configurar los productos que se generan en el pedido de venta
        # Datos de configuración para compras
        'diesel': fields.many2one("res.partner", "Proveedor de Diesel"),
        'casetas': fields.many2one("res.partner", "Proveedor de peage"),
    }
fleosa_config()
