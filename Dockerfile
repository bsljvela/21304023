# Utiliza la imagen oficial de Python para Django
FROM python:3.12.6 AS backend


# Establecer directorio de trabajo para el backend
WORKDIR /app


# Instalar dependencias necesarias para Python
RUN apt-get update && apt-get install -y netcat-openbsd --no-install-recommends \
    default-libmysqlclient-dev build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Copiar el archivo de dependencias e instalar
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copiar el proyecto de Django
COPY backend /app


# Dar permisos de ejecución -rwxr-xr-x
RUN chmod +x /app/backend-entrypoint.sh


# Configurar el script como punto de entrada
ENTRYPOINT ["sh", "/app/backend-entrypoint.sh"]


# Comando por defecto para iniciar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# --- Construcción del Frontend ---
FROM node:18 AS frontend


# Establecer directorio de trabajo para el frontend
WORKDIR /frontend


# Copiar archivos del frontend
COPY frontend/package*.json /frontend/
RUN npm install


# Copiar el resto del código del frontend y construir
COPY frontend /frontend
RUN npm run build


# Servir la aplicación React estática con NGINX
FROM nginx:alpine AS production


# Copiar el build de React al directorio de NGINX
COPY --from=frontend /frontend/dist/ /usr/share/nginx/html


# Copiar la configuración personalizada de NGINX
COPY nginx.conf /etc/nginx/conf.d/default.conf


# Exponer el puerto 80
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]