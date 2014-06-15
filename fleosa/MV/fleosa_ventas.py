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
import decimal_precision as dp

class fleosa_mv_sale(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    def confirmar_envio(self, cr, uid, ids, context=None):
        return True
        
    def calcular_impuestos(self, cr, uid, ids, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return self.write(cr, uid, ids, res[order.id])
    
    _columns = {
        'carta_porte_id': fields.many2one("fleosa.ml.cp", "Carta Porte", readonly=True),
        'partner_destinatario_id': fields.many2one("res.partner", "Destinatario", required=True, states={'draft': [('readonly', False)]}),
        'partner_direccion_remitente': fields.many2one("res.partner.address", "Dirección Remitente", required=True, states={'draft': [('readonly', False)]}),
        'partner_order_id': fields.many2one('res.partner.address', 'Ordering Contact', readonly=True, states={'draft': [('readonly', False)]}, help="The name and address of the contact who requested the order or quotation."),
        'amount_untaxed': fields.float("Base", readonly=True, multi='sums', help="Total antes de impuestos."),
        'amount_tax': fields.float("Impuestos", readonly=True, multi='sums', help="Impuestos."),
        'amount_total': fields.float("Base", readonly=True, multi='sums', help="Total con impuestos."),
        'state': fields.selection([
            ('draft', 'Quotation'),
            ('waiting_date', 'Waiting Schedule'),
            ('viaje','En curso de viaje'),
            ('manual', 'To Invoice'),
            ('progress', 'In Progress'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
            ], 'Order State', readonly=True, help="Gives the state of the quotation or sales order. \nThe exception state is automatically set when a cancel operation occurs in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception). \nThe 'Waiting Schedule' state is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
    }
    
fleosa_mv_sale()
