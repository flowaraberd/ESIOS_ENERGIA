class CONFIG:
    config_db = {
        "host": "localhost", # IP de la donde esta la Base de datos
        "port": "3306", # En el puerto que esta escuchando, por defecto en 3306
        "user": "root", # Para conectarse a la BD.
        "password": "Aa123456@", # Para conectarse a la BD.
        "database": "example" # Nombre de la Base de datos.
    }
    # Ruta donde se encuentran todos los enlaces que se leerá
    path_urls_channel = "./urls_channel.txt"
    # Ruta donde se encuentra el archivo para regustrar los errores.
    PATH_FILE_LOG = "./logs/logs_error.log"
