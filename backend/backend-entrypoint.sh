#!/bin/bash
set -e


# Esperar a la base de datos (opcional)
until nc -z -v -w30 db 3306; do
  echo "Esperando a que la base de dato esté disponible..."
  sleep 20
done
echo "¡Base de datos disponible!"


# Ejecutar migraciones
python manage.py migrate


echo "¡Migraciones ejecutadas exitosamente!"


# Recolectar archivos estáticos
#python manage.py collectstatic --noinput


# Ejecutar el servidor
exec "$@"
