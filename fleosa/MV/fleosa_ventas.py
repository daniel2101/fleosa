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

class fleosa_mv_sale(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'carta_porte_id': fields.many2one("fleosa.ml.cp", "Carta Porte", readonly=True),
        'partner_destinatario_id': fields.many2one("res.partner", "Destinatario", required=True, states={'draft': [('readonly', False)]}),
        'partner_direccion_remitente': fields.many2one("res.partner.address", "Dirección Remitente", required=True, states={'draft': [('readonly', False)]}),
        'partner_order_id': fields.many2one('res.partner.address', 'Ordering Contact', readonly=True, states={'draft': [('readonly', False)]}, help="The name and address of the contact who requested the order or quotation."),
        #'state': fields.selection(),
    }
    
fleosa_mv_sale()
