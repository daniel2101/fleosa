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

class fleosa_ml_cp(osv.osv):

    _name = "fleosa.ml.cp"
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'borrador',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'sale.order'),
        })
        return super(fleosa_ml_cp, self).copy(cr, uid, id, default, context=context)
        
    def unlink(self, cr, uid, ids, context=None):
        cartas_porte = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in cartas_porte:
            if s['state'] in ['borrador']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(('Acción Invalida !'), ('Solo pueden ser eliminadas las cartas porte en borrador.'))
        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
    
    def on_change_unidad(self, cr, uid, ids, part):
        if not part:
            return {'value': {'unidad': False, 'operador': False, 'contenedor': False}}
        unidad = self.pool.get('fleosa.mu.unidades').browse(cr, uid, part)
        return {'value': {'operador': unidad.operador.id, 'contenedor': unidad.contenedor.id}}
    
    def on_change_remitente(self, cr, uid, ids, part):
        if not part:
            return {'value': {'partner_invoice_id': False}}
        addr = self.pool.get('res.partner').address_get(cr, uid, [part], ['delivery'])
        direccion = self.pool.get('res.partner.address').browse(cr,uid,addr['delivery'])
        origen = ("%s, %s")%(direccion.city, direccion.state_id.name)
        return {'value': {'partner_invoice_id': addr['delivery'], 'origen': origen}}
    
    def on_change_destinatario(self, cr, uid, ids, part):
        if not part:
            return {'value': {'partner_shipping_id': False}}
        addr = self.pool.get('res.partner').address_get(cr, uid, [part], ['delivery'])
        direccion = self.pool.get('res.partner.address').browse(cr,uid,addr['delivery'])
        destino = ("%s, %s")%(direccion.city,direccion.state_id.name)
        return {'value': {'partner_shipping_id': addr['delivery'], 'destino': destino}}
        
    def button_generar_so(self, cr, uid, ids, context=None):
        carta_porte = self.read(cr, uid, ids, context=context)
        cp = carta_porte[0]
        addr = self.pool.get('res.partner').address_get(cr, uid, [cp['partner_id'][0]], ['invoice'])
        company = self.pool.get('res.company').search(cr, uid, [],limit=1)
        tienda = self.pool.get('sale.shop').search(cr, uid, [],limit=1)
        lista = self.pool.get('product.pricelist').search(cr, uid, [('type', '=', 'sale')],limit=1)
        vals = {
            'carta_porte_id': cp['id'],
            'name': cp['name'],
            'partner_id': cp['partner_id'][0],
            'partner_invoice_id': addr['invoice'],
            'partner_direccion_remitente': cp['partner_invoice_id'][0],
            'partner_destinatario_id': cp['destinatario'][0],
            'partner_shipping_id': cp['partner_shipping_id'][0],
            'user_id': uid,
            'company_id': company[0],
            'shop_id': tienda[0],
            'pricelist_id': lista[0],
        }
        so = self.pool.get('sale.order')
        so.create(cr, uid, vals, context=context)
        return self.write(cr, uid, ids, {'state': 'ventas'})
        
    _columns = {
        'name': fields.char("Referencia", size=50, required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'user_id': fields.many2one("res.users", "Logistica"),
        'date_order': fields.date("Fecha de Pedido", required=True, readonly=True, select=True, states={'borrador': [('readonly', False)]}),
        'partner_id': fields.many2one("res.partner","Remitente", required=True, help="Seleccione el remitente.", readonly=True, states={'borrador': [('readonly', False)]}),
        'partner_invoice_id': fields.many2one("res.partner.address","Dirección", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'destinatario': fields.many2one("res.partner", "Destinatario", required="True", help="Seleccione el destinatario.", readonly=True, states={'borrador': [('readonly', False)]}),
        'partner_shipping_id': fields.many2one("res.partner.address","Dirección", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'origen': fields.char("Recoger en", size=50, readonly=True, states={'borrador': [('readonly', False)]}),
        'destino': fields.char("Entregar en", size=50, readonly=True, states={'borrador': [('readonly', False)]}),
        'fecha_embarque': fields.datetime("Fecha programada de embarque", readonly=True, states={'borrador': [('readonly', False)]}),
        'fecha_entrega': fields.datetime("Fecha programada de entrega", readonly=True, states={'borrador': [('readonly', False)]}),
        'producto_transportar': fields.many2one("product.product", "Producto a Transportar", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'cantidad': fields.float("Cantidad programada", digits=(6,2), readonly=True, states={'borrador': [('readonly', False)]}),
        'valor_declarado': fields.float("Valor Declarado", digits=(8,2), readonly=True, states={'borrador': [('readonly', False)]}),
        'sellos': fields.char("Sellos", size=100, readonly=True, states={'borrador': [('readonly', False)]}),
        'remision': fields.char("Remision", size=100, readonly=True, states={'borrador': [('readonly', False)]}),
        'unidad': fields.many2one("fleosa.mu.unidades", "Unidad", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'contenedor': fields.many2one("fleosa.mu.contenedores", "Contenedor", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'operador': fields.many2one("hr.employee", "Operador", required=True, readonly=True, states={'borrador': [('readonly', False)]}),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('ventas', 'En ventas'),
            ('en_curso', 'En curso'),
            ('entregado', 'Entregado'),
            ('cancelado', 'Cancelado')
            ],"Estado"),
        }
    _defaults = {
        'state': 'borrador',
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'sale.order'),
        'date_order': fields.date.context_today,
        'user_id': lambda obj, cr, uid, context: uid,
        'state': 'borrador',
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'El número de orden debe de ser unico!'),
    ]
    _order = 'name desc'
fleosa_ml_cp()
