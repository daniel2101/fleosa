#!/bin/bash

if [ -z $1 ]; then
        echo "ERROR: Falta de parametro el nombre del modulo."
        exit 1;
fi
clear
echo "Borrando Archivos temporales..."
rm `find | grep /*~`
echo "Borrando Modulo Anterior..."
rm -R /opt/openerp/server/openerp/addons/$1
echo "Copiando Modulo Nuevo..."
cp -R $1 /opt/openerp/server/openerp/addons/$1
echo "Configurando Permisos..."
chmod -R 755 /opt/openerp/server/openerp/addons/$1
echo "Borrando Log..."
rm /var/log/openerp/openerp-server.log
echo "Reiniciando Servidor..."
service openerp-server restart
echo "Terminado :D"
sleep 3
cat /var/log/openerp/openerp-server.log
