<VirtualHost *>
    ServerName example.com

    WSGIDaemonProcess flaskr user=user1 group=group1 threads=5
    WSGIScriptAlias / /var/www/FlaskDB/flaskr/flaskr.wsgi

    <Directory /var/www/FlaskDB/flaskr>
        WSGIProcessGroup flaskr
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>