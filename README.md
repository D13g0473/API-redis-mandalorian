# API-redis-mandalorian

# Descripción: 
La api esta diseñada en python version detallada más adelante y el frontend esta diseñado en quasar framework de vue. 
Espero sea de su agrado. 
Cualquier consulta a disposicion.
 
# Version de Python

```
 3.10.12
```
# Version de node 

```
20.12.2
```

# Comandos para levantar la api de python 

In API-redis-mandalorian dir run 
```bash 
python3 api.py
```

# Comando para levantar la aplicación de quasar 

# Cambiamos al directorio "mando-app"
```bash 
cd mando-app
```

# Seleccionamos la versión correcta de node.
```bash 
nvm use 20.12.2
```

# Instalamos dependencias
```bash
npm install 
```
# Lecantamos el servidor de Quasar
```bash
quasar dev
```

En la url "http://localhost:9000/#/" deberia aparecer 
![image](https://github.com/user-attachments/assets/5974197a-99c3-4bef-a59a-23cf38aaf62b)

Si el puerto es diferente a 9000, debemos actualizar en el cors de la api de python, para que permita solicitudes de este sitio.  

de:
```py
CORS(app, origins=["http://localhost:9000"], allow_headers=["Content-Type"], methods=["GET", "POST"])
```
a: 
```py
CORS(app, origins=["http://localhost:900X"], allow_headers=["Content-Type"], methods=["GET", "POST"])
```
Donde 900X es el puerto en el que se levanto la app de quasar. 
