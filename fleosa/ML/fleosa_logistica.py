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
            'partner_direccion_remitente': cp['partner_invoice_id'][0], #Origen
            'partner_destinatario_id': cp['destinatario'][0],
            'partner_shipping_id': cp['partner_shipping_id'][0], #Destino
            'user_id': uid,
            'company_id': company[0],
            'shop_id': tienda[0],
            'pricelist_id': lista[0],
        }
        so = self.pool.get('sale.order')
        id_so = so.create(cr, uid, vals, context=context)
        origen = self.pool.get('res.partner.address').browse(cr,uid,vals['partner_direccion_remitente'])
        destino = self.pool.get('res.partner.address').browse(cr,uid,vals['partner_shipping_id'])
        ciudad_origen = origen.city
        ciudad_destino = destino.city
        estado_origen = origen.state_id.id
        estado_destino = destino.state_id.id
        order_line = self.pool.get('sale.order.line') #Objeto sale.order.line
        l = [0,0,0,0,0,0,0]
        #Buscar y agregar FLETE
        producto = self.pool.get('product.product').search(cr, uid, [('origen_ciudad','=', ciudad_origen), ('destino_ciudad','=', ciudad_destino), ('origen_estado_id','=', estado_origen), ('destino_estado_id','=',estado_destino)], limit=1)
        lineas1 = order_line.product_id_change(cr, uid, id_so, vals['pricelist_id'], producto[0],partner_id=uid)
        lineas1['value'].update({'order_id': id_so, 'product_id': producto[0], 'product_uos_qty': '1.000'})
        l[1] = order_line.create(cr,uid, lineas1['value'], context=context)
        #Buscar y agregar SEGURO
        producto = self.pool.get('product.product').search(cr, uid, [('name','=',"SEGURO")], limit=1)
        lineas2 = order_line.product_id_change(cr, uid, id_so, vals['pricelist_id'], producto[0],partner_id=uid)
        lineas2['value'].update({'order_id': id_so, 'product_id': producto[0], 'product_uos_qty': '1.000'})
        l[2] = order_line.create(cr,uid, lineas2['value'], context=context)
        #Buscar y agregar MANIOBRAS
        producto = self.pool.get('product.product').search(cr, uid, [('name','=',"MANIOBRAS")], limit=1)
        lineas3 = order_line.product_id_change(cr, uid, id_so, vals['pricelist_id'], producto[0],partner_id=uid)
        lineas3['value'].update({'order_id': id_so, 'product_id': producto[0], 'product_uos_qty': '1.000'})
        l[3] = order_line.create(cr,uid, lineas3['value'], context=context)
        #Buscar y agregar REPARTO
        producto = self.pool.get('product.product').search(cr, uid, [('name','=',"REPARTO")], limit=1)
        lineas4 = order_line.product_id_change(cr, uid, id_so, vals['pricelist_id'], producto[0],partner_id=uid)
        lineas4['value'].update({'order_id': id_so, 'product_id': producto[0], 'product_uos_qty': '1.000'})
        l[4] = order_line.create(cr,uid, lineas4['value'], context=context)
        #Buscar y agregar AUTOPISTAS
        producto = self.pool.get('product.product').search(cr, uid, [('name','=',"AUTOPISTAS")], limit=1)
        lineas5 = order_line.product_id_change(cr, uid, id_so, vals['pricelist_id'], producto[0],partner_id=uid)
        lineas5['value'].update({'order_id': id_so, 'product_id': producto[0], 'product_uos_qty': '1.000'})
        l[5] = order_line.create(cr,uid, lineas5['value'], context=context)
        #Buscar y agregar OTROS
        producto = self.pool.get('product.product').search(cr, uid, [('name','=',"OTROS")], limit=1)
        lineas6 = order_line.product_id_change(cr, uid, id_so, vals['pricelist_id'], producto[0],partner_id=uid)
        lineas6['value'].update({'order_id': id_so, 'product_id': producto[0], 'product_uos_qty': '1.000'})
        l[6] = order_line.create(cr,uid, lineas6['value'], context=context)
        if (l[1] and l[2] and l[3] and l[4] and l[5] and l[6]):
            #Insertar Impuestos
            lineas = [lineas1, lineas2, lineas3, lineas4, lineas5, lineas6]
            cont=1
            for li in lineas:
                for i in li['value']['tax_id']:
                    cr.execute("INSERT INTO sale_order_tax VALUES (%s, %s)",(l[cont], i))
                cont+=1
            return self.write(cr, uid, ids, {'state': 'ventas'})
        else: raise osv.except_osv(lineas1['warning']['title'], lineas1['warning']['message'])
        return False
        
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
