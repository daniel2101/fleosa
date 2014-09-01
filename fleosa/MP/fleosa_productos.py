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

class fleosa_mp_productos(osv.osv):

    _inherit = "product.product"
    
    def _get_default_pais_id(self, cr, uid, context=None):
        country_obj = self.pool.get('res.country')
        ids = country_obj.search(cr, uid, [ ( 'code', '=', 'MX' ), ], limit=1)
        id = ids and ids[0] or False
        return id
        
    def onchange_tipo(self, cursor, user, ids, value):
        return {'value': {}}
        
    def write(self, cr, uid, ids, vals, context=None):
        try:
            vals['origen_ciudad'] = vals['origen_ciudad'].upper()
            vals['destino_ciudad'] = vals['destino_ciudad'].upper()
        except: 
            return super(fleosa_mp_productos, self).write(cr, uid, ids, vals, context=context)
        return super(fleosa_mp_productos, self).write(cr, uid, ids, vals, context=context)
        
    def create(self, cr, uid, vals, context=None):
        if vals.get('origen_ciudad', False) and vals.get('destino_ciudad', False):
            vals['origen_ciudad'] = vals['origen_ciudad'].upper()
            vals['destino_ciudad'] = vals['destino_ciudad'].upper()
        return super(fleosa_mp_productos, self).create(cr, uid, vals, context=context)
        
    _columns = {
        'tipo_flete': fields.boolean("Es flete"),
        'pais_id': fields.many2one("res.country","Pais", readonly=True),
        'origen_ciudad': fields.char("Ciudad", size=50),
        'origen_estado_id': fields.many2one("res.country.state","Estado", domain="[('country_id','=',pais_id)]", help="Si es un producto de tipo flete, selecciona el estado de origen."),
        'destino_ciudad': fields.char("Ciudad", size=50),
        'destino_estado_id': fields.many2one("res.country.state","Estado", domain="[('country_id','=',pais_id)]", help="Si es un producto de tipo flete, selecciona el estado de destino."),
    }
    
    _defaults = {
        'pais_id': _get_default_pais_id,
    }
    
fleosa_mp_productos()
