import json

from mysql import connector
from config.config import CONFIG
from control.logs import capture_error
from control.database import (
    is_table_exists,
    is_esios_energia_exists,
    create_table_esios_energia
)
from esios_api_connect import listar_datos
import requests


def set_connect():
    connect = connector.connect(**CONFIG.config_db)
    cursor = connect.cursor()

    ## PREPARAR LA LLAMADA A LA API
    url = 'https://api.esios.ree.es/indicators/1001'
    headers = {'Accept': 'application/json; application/vnd.esios-api-v2+json',
               'Content-Type': 'application/json',
               'Host': 'api.esios.ree.es',
               'x-api-key': '469ebcd49d946e165feb6d068551c2b008aa2ed083d27805750f8288a9b57327'}

    ## HACER LA PETICION
    response = requests.get(url, headers=headers)

    # Para verificar si la tabla existe, en caso de no,
    # realiza una llamada a las funciones que esten en "call"
    is_table_exists(
        cursor=cursor,
        call=[
            create_table_esios_energia
        ]
    )

    """Configurar geolocalizacion del precio Mediande el GeoID: 
        8741 - Peninsula, 
        8742 - Canarias, 
        8743 - Baleares, 
        8744 - Ceuta, 
        8745 - Melilla
    """
    migeoid_peninsula = 8741
    migeoid_ceuta = 8744
    migeoid_melilla = 8745

    ## Si la respuesta desde la web de ESIOS es 200 (OK)
    if response.status_code == 200:
        try:
            datos_peninsula = listar_datos(migeoid=migeoid_peninsula, response=response)
            datos_ceuta = listar_datos(migeoid=migeoid_ceuta, response=response)
            datos_melilla = listar_datos(migeoid=migeoid_melilla, response=response)

            is_esios_energia_exists(
                cursor=cursor,
                d_peninsula=json.dumps(datos_peninsula),
                d_ceuta=json.dumps(datos_ceuta),
                d_melilla=json.dumps(datos_melilla),
                publish_in=datos_peninsula['PublishIn']
            )
        except Exception as error:
            capture_error(str(error), '---------- set connect -----------')

        connect.commit()
        connect.close()
        print("Todos datos guardadas.")
