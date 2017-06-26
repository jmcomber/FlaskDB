<VirtualHost *>
    ServerName query17-3.ing.puc.cl

    WSGIDaemonProcess flaskr user=algo group=algo threads=5
    WSGIScriptAlias / /var/www/FlaskDB/flaskr/flaskr.wsgi

    <Directory /var/www/FlaskDB/flaskr>
        WSGIProcessGroup flaskr
        WSGIScriptReloading On
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>