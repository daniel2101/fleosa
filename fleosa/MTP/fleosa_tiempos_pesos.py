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

class fleosa_mtp_pesos_multi(osv.osv):
    _name = "fleosa.mtp.pesos.multi"
    
    _columns = {
        'name': fields.char("Descripción", size=100, required=True),
        'peso': fields.integer("Peso", required=True),
    }
fleosa_mtp_pesos_multi()


class fleosa_mtp_pesos(osv.osv):

    _name="fleosa.mtp.pesos"
    

    def calcular_pesos(self, cr, uid, ids, pto, ptd, pbo, pbd, context):
        res={}
        res['peso_neto_o'] = pbo - pto
        res['peso_neto_d'] = pbd - ptd
        res['dif_peso_tara'] = pto - ptd
        res['dif_peso_bruto'] = pbo - pbd
        res['dif_peso_neto'] = res['peso_neto_o'] - res['peso_neto_d']
        res['toneladas_entregadas'] = res['peso_neto_d']
        self.write(cr, uid, ids, res)
        return {'value':res}
    
    def terminar(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'terminado'})

    
    
    _columns = {
    'name': fields.many2one("fleosa.ml.cp", 'Carta Porte', readonly=True, required=True),
    'unidad': fields.many2one("fleosa.mu.unidades", 'Unidad', readonly=True, required=True),
    'tanque': fields.many2one("fleosa.mu.contenedores", 'Pipa', readonly=True, required=True),
    'cliente': fields.many2one("res.partner", 'Cliente', readonly=True, required=True),
    'producto': fields.many2one("product.product", 'Producto', readonly=True, required=True),
    'peso_tara_o':fields.float("Peso Tara origen"),
    'peso_tara_d': fields.float("Peso Tara destino"),
    'peso_bruto_o': fields.float("Peso Bruto origen"),
    'peso_bruto_d': fields.float("Peso Bruto destino"),
    'peso_neto_o': fields.float("Peso Neto origen", readonly=True),
    'peso_neto_d': fields.float("Peso Neto destino", readonly=True),
    'dif_peso_bruto': fields.float("Diferencia en peso bruto", readonly=True),
    'dif_peso_neto': fields.float("Diferencia en peso neto", readonly=True),
    'dif_peso_tara': fields.float("Diferencia en peso tara", readonly=True),
    'toneladas_entregadas': fields.float("Total de Toneladas Entregadas", readonly=True),
    'multi_pesos': fields.many2many("fleosa.mtp.pesos.multi", "fleosa_mtp_pesos_rel", "pesos_id", "pesos_multi_id"),
    'state': fields.selection((
        ('pendiente', 'Pendiente'),
        ('terminado', 'Terminado')
    ), "Estado"),
    'observ_ent': fields.text("Observaciones"),
    }
    
    _order = 'name desc'
    

fleosa_mtp_pesos()

class fleosa_mtp_tiempos(osv.osv):
    _name="fleosa.mtp.tiempos"
    
    def entrada(self, cr, uid, ids, context=None):
        cp = self.browse(cr, uid, ids)[0].name
        #Poner la carta porte estado entregado
        self.pool.get("fleosa.ml.cp").write(cr, uid, [cp.id], {'state':'entregado'})
        #Poner la unidad estado en pension
        self.pool.get("fleosa.mu.unidades").write(cr, uid, [cp.unidad.id], {'state':'pension'})
        #Poner el contenedor estado en pension
        self.pool.get("fleosa.mu.contenedores").write(cr, uid, [cp.contenedor.id], {'state':'pension'})
        return self.write(cr, uid, ids, {'state': 'terminado'})
    
    def enviar(self, cr, uid, ids, context=None):
        cp = self.browse(cr, uid, ids)[0].name
        #Poner la carta porte estado en curso
        self.pool.get("fleosa.ml.cp").write(cr, uid, [cp.id], {'state':'en_curso'})
        #Poner la unidad estado en viaje
        self.pool.get("fleosa.mu.unidades").write(cr, uid, [cp.unidad.id], {'state':'viaje'})
        #Poner el contenedor estado en viaje
        self.pool.get("fleosa.mu.contenedores").write(cr, uid, [cp.contenedor.id], {'state':'viaje'})
        return self.write(cr, uid, ids, {'state': 'viaje'})

    _columns={
    'name': fields.many2one("fleosa.ml.cp", 'Carta Porte', readonly=True, required=True),
    'fecha_salida_pension': fields.datetime("Salida de la pension"),
    'fecha_salida_entrega': fields.datetime("Salida a la entrega"),
    'fecha_llega_entrega': fields.datetime("Entrega al cliente"),
    'fecha_llega_pension': fields.datetime("Llegada a la pension"),
    'state': fields.selection((
        ('pension','Pensión'),
        ('viaje', 'En viaje'),
        ('terminado', 'Terminado')
    ), "Estado"),
    }
    _order = 'name desc'
fleosa_mtp_tiempos()

class fleosa_mtp(osv.osv):

    _name="fleosa.mtp"
    

    def calcular_pesos(self, cr, uid, ids, pto, ptd, pbo, pbd, context):
        res={}
        res['peso_neto_o'] = pbo - pto
        res['peso_neto_d'] = pbd - ptd
        res['dif_peso_tara'] = pto - ptd
        res['dif_peso_bruto'] = pbo - pbd
        res['dif_peso_neto'] = res['peso_neto_o'] - res['peso_neto_d']
        res['toneladas_entregadas'] = res['peso_neto_d']
        self.write(cr, uid, ids, res)
        return {'value':res}


    def entrada(self, cr, uid, ids, context=None):
        cp = self.browse(cr, uid, ids)[0].name
        #Poner la carta porte estado entregado
        self.pool.get("fleosa.ml.cp").write(cr, uid, [cp.id], {'state':'entregado'})
        #Poner la unidad estado en pension
        self.pool.get("fleosa.mu.unidades").write(cr, uid, [cp.unidad.id], {'state':'pension'})
        #Poner el contenedor estado en pension
        self.pool.get("fleosa.mu.contenedores").write(cr, uid, [cp.contenedor.id], {'state':'pension'})
        return self.write(cr, uid, ids, {'state': 'terminado'})
    
    def enviar(self, cr, uid, ids, context=None):
        cp = self.browse(cr, uid, ids)[0].name
        #Poner la carta porte estado en curso
        self.pool.get("fleosa.ml.cp").write(cr, uid, [cp.id], {'state':'en_curso'})
        #Poner la unidad estado en viaje
        self.pool.get("fleosa.mu.unidades").write(cr, uid, [cp.unidad.id], {'state':'viaje'})
        #Poner el contenedor estado en viaje
        self.pool.get("fleosa.mu.contenedores").write(cr, uid, [cp.contenedor.id], {'state':'viaje'})
        return self.write(cr, uid, ids, {'state': 'viaje'})
    
    _columns = {
    #GENERAL
    'name': fields.many2one("fleosa.ml.cp", 'Carta Porte', readonly=True, required=True),
    'unidad': fields.many2one("fleosa.mu.unidades", 'Unidad', readonly=True, required=True),
    'tanque': fields.many2one("fleosa.mu.contenedores", 'Pipa', readonly=True, required=True),
    'cliente': fields.many2one("res.partner", 'Cliente', readonly=True, required=True),
    'destinatario': fields.many2one("res.partner","Destinatario", readonly=True),
    'producto': fields.many2one("product.product", 'Producto', readonly=True, required=True),
    #PESOS
    'peso_tara_o':fields.float("Peso Tara origen"),
    'peso_tara_d': fields.float("Peso Tara destino"),
    'peso_bruto_o': fields.float("Peso Bruto origen"),
    'peso_bruto_d': fields.float("Peso Bruto destino"),
    'peso_neto_o': fields.float("Peso Neto origen", readonly=True),
    'peso_neto_d': fields.float("Peso Neto destino", readonly=True),
    'dif_peso_bruto': fields.float("Diferencia en peso bruto", readonly=True),
    'dif_peso_neto': fields.float("Diferencia en peso neto", readonly=True),
    'dif_peso_tara': fields.float("Diferencia en peso tara", readonly=True),
    'toneladas_entregadas': fields.float("Total de Toneladas Entregadas", readonly=True),
    'multi_pesos': fields.many2many("fleosa.mtp.pesos.multi", "fleosa_mtp_pesos_multi_rel", "mtp_id", "pesos_multi_id"),
    #TIEMPOS
    'fecha_salida_pension': fields.datetime("Salida de la pension"),
    'fecha_salida_entrega': fields.datetime("Salida del origen"),
    'fecha_llega_entrega': fields.datetime("Llegada al destino"),
    'fecha_llega_pension': fields.datetime("Llegada a la pension"),
    'state': fields.selection((
        ('pendiente','Pendiente'),
        ('viaje', 'En viaje'),
        ('terminado', 'Terminado')
    ), "Estado"),
    #GENERAL
    'observ_ent': fields.text("Observaciones"),
    }
    
    _order = 'name desc'
    

fleosa_mtp()
