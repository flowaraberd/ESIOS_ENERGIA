import requests
import json
import statistics
from datetime import datetime
import sys


def listar_datos(migeoid, response):
  ## Variables para uso interno
  bajomedia =  0
  proximahorabm = 0
  itemsbajomedia = int(0)
  horaejecucion = datetime.now().hour

  ## CONVERTIR A DISCCIONARIO PYTHON
  json_data = json.loads(response.text)

  ## QUEDARME CON EL LISTADO DE VALORES SOLO
  valores = json_data['indicator']['values']

  ## FILTRAR LOS VALORES POR GEOID
  valores_geoid = [x for x in valores if x['geo_id'] == migeoid ]

  ## SACAR DENTRO DEL LISTADO DE VALORES SOLO EL PRECIO
  precios = [x['value'] for x in valores_geoid ]
  ## SACAR MAX MIN Y MED DEL LISTADO DE VALORES
  valor_min = min(precios)
  valor_max = max(precios)
  valor_med = round(statistics.mean(precios),2)

  valor_fecha = []


  ## Recorrer los valores uno por uno para sacar la informacion que me interesa
  for t_valor in valores_geoid:

    # Obtener el valor en el tiempo
    valor_fecha.append((round(t_valor['value']), t_valor['datetime']))

    ## Si hay parametros en la linea de comandos y concretamente es -v (solo para debug)
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
      ## Imprimir la linea por la consola
      print(t_valor)
    ## Sacar la hora del valor y convertirla a objeto datetime
    t_valor_date = datetime.fromisoformat(t_valor['datetime'])
    # print(f"Valor: {t_valor['value']}, Tiempo: {t_valor['datetime']}")
    ## Si el precio esta por debajo de la media ...
    if t_valor['value'] < valor_med:
      ## Incremento el contador de numero de horas por debajo de la media
      itemsbajomedia += 1
      ## Si ademas es en el futuro y no he pillado aun la proxima hora bajo la media ....
      if t_valor_date.hour > horaejecucion and not proximahorabm:
        ## Me apunto en mi variable la hora
        proximahorabm = t_valor_date
    ## Si la hora del precio es ahora
    if t_valor_date.hour == horaejecucion:
      ## Me lo apunto como valor actual
      valor_act = t_valor['value']
      ## Y pongo en la variable bajomedia true o false para saber si esta por debajo de la media
      bajomedia = valor_act < valor_med


  json_datos = {
    'Actual': str(valor_act),
    'Maximo': str(valor_max),
    'Minimo': str(valor_min),
    'Media': str(valor_med),
    'BajoMedia': str(bajomedia).lower(),
    'ProximaBM': str(proximahorabm),
    'HorasBM': str(itemsbajomedia),
    'ValorFecha': valor_fecha,
    'PublishIn': valor_fecha[0][1]
  }
  # print(proximahorabm)
  return json_datos


