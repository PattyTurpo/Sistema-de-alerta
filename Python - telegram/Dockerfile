# Imagen base de PHP con Apache
FROM php:8.2-apache

# Copiar los archivos al contenedor
COPY . /var/www/html/

# Dar permisos a uploads y videos
RUN chmod -R 777 /var/www/html/uploads \