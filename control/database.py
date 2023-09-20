from datetime import datetime
from control.logs import capture_error


# Verificar si la tabla a crear existe, antes de crearla.
def is_table_exists(**data):
    try:
        cursor = data['cursor']
        call = data['call']
        for llamar in call:
            datos = llamar()
            sql = f"SHOW TABLES LIKE '{datos['table_name']}'"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if len(resultado) <= 0:
                cursor.execute(datos['sql'])
                print(f"Creando tabla... {datos['table_name']}")
    except Exception as error:
        capture_error(str(error), '---------- is_table_exists -----------')


# Estructura de la Tabla.
def create_table_esios_energia() -> dict:
    table_name = "esios_energia"
    sql = """
    CREATE TABLE esios_energia (
    id int AUTO_INCREMENT,
    d_peninsula TEXT not null,
    d_ceuta TEXT not null,
    d_melilla TEXT not null,
    publish_in TIMESTAMP, 
    PRIMARY KEY (id)
    );
    """
    return dict(table_name=table_name, sql=sql)


# Para verificar si el ID existe en la Base de datos
# antes de insertarlo.
def is_esios_energia_exists(cursor, d_peninsula: str, d_ceuta: str, d_melilla: str, publish_in: str):
    sql = f"SELECT 1 FROM esios_energia WHERE publish_in='{publish_in}'"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado) <= 0:
        sql = f"INSERT INTO esios_energia(d_peninsula, d_ceuta, d_melilla, publish_in) VALUES ('{d_peninsula}', '{d_ceuta}', '{d_melilla}', '{publish_in}')"
        cursor.execute(sql)
