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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from osv import osv, fields
import decimal_precision as dp

class fleosa_mv_sale(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    def confirmar_envio(self, cr, uid, ids, context=None):
        vals = {'state': 'viaje'}
        so = self.browse(cr, uid, ids, context=context)[0]
        po = self.pool.get('purchase.order')
        product = self.pool.get('product.product')
        #Crear orden de compra de DIESEL
        producto_ids = product.search(cr, uid, [('name','=', 'DIESEL')], limit=1)
        if not producto_ids:
            raise osv.except_osv("Advertencia", "En productos no existe un producto llamado: DIESEL")
        producto = product.browse(cr, uid, producto_ids)[0]
        partner = producto.seller_ids[0].name
        if not partner:
            raise osv.except_osv("Advertencia", "El producto DIESEL no tiene configurado un proveedor.")
        partner_add = self.pool.get('res.partner').address_get(cr, uid, [partner.id], ['invoice'])
        order_line = self.pool.get('purchase.order.line')
        vals_po = {
            'origin': so.name,
            'partner_id': partner.id,
            'partner_address_id': partner_add['invoice'],
            'pricelist_id': partner.property_product_pricelist_purchase.id,
            'location_id': partner.property_stock_supplier.id,
        }
        id_po = po.create(cr, uid, vals_po)
        linea = order_line.onchange_product_id(cr, uid, id_po, vals_po['pricelist_id'], producto.id,1.0, producto.uom_po_id.id, vals_po['partner_id'], date_order = fields.date.context_today(self, cr, uid, context=None), context=None)
        linea['value'].update({'order_id': id_po, 'product_id': producto.id})
        l_id = order_line.create(cr,uid, linea['value'], context=context)
        for i in linea['value']['taxes_id']:
            cr.execute("INSERT INTO purchase_order_taxe VALUES (%s, %s)",(l_id, i))
        #CREAR REGISTRO DE PESOS
        pesos_obj = self.pool.get("fleosa.mtp.pesos")
        vals_pesos = {
            'name': so.carta_porte_id.id,
            'unidad': so.carta_porte_id.unidad.id,
            'tanque': so.carta_porte_id.contenedor.id,
            'cliente': so.carta_porte_id.partner_id.id,
            'producto': so.carta_porte_id.producto_transportar.id,
            'state': 'pendiente',
        }
        pesos_id = pesos_obj.create(cr, uid, vals_pesos)
        #CREAR REGISTRO DE TIEMPOS
        tiempos_obj = self.pool.get("fleosa.mtp.tiempos")
        vals_tiempos = {
            'name': so.carta_porte_id.id,
            'state': 'pension',
        }
        tiempos_id = tiempos_obj.create(cr, uid, vals_tiempos)
        vals['pesos_id'] = pesos_id
        vals['tiempos_id'] = tiempos_id
        return self.write(cr, uid, ids, vals)
        
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
        'pesos_id': fields.many2one("fleosa.mtp.pesos", "Registro de Pesos", readonly=True),
        'tiempos_id': fields.many2one("fleosa.mtp.tiempos", "Registro de Tiempos", readonly=True),
        'partner_destinatario_id': fields.many2one("res.partner", "Destinatario", required=True, states={'draft': [('readonly', False)]}),
        'partner_direccion_remitente': fields.many2one("res.partner.address", "Dirección Remitente", required=True, states={'draft': [('readonly', False)]}),
        'partner_order_id': fields.many2one('res.partner.address', 'Ordering Contact', readonly=True, states={'draft': [('readonly', False)]}, help="The name and address of the contact who requested the order or quotation."),
        'amount_untaxed': fields.float("Base", readonly=True, multi='sums', help="Total antes de impuestos."),
        'amount_tax': fields.float("Impuestos", readonly=True, multi='sums', help="Impuestos."),
        'amount_total': fields.float("Base", readonly=True, multi='sums', help="Total con impuestos."),
        'state': fields.selection([
            ('draft', 'Cotización'),
            ('waiting_date', 'Esperando Fecha'),
            ('viaje','En Viaje'),
            ('manual', 'Para Facturar'),
            ('progress', 'En Progreso'),
            ('shipping_except', 'Excepción de Envio'),
            ('invoice_except', 'Excepción de Factura'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
            ], 'Order State', readonly=True, help="Gives the state of the quotation or sales order. \nThe exception state is automatically set when a cancel operation occurs in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception). \nThe 'Waiting Schedule' state is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
        'order_line': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)], 'viaje':[('readonly',False)]}),
    }
    
fleosa_mv_sale()
