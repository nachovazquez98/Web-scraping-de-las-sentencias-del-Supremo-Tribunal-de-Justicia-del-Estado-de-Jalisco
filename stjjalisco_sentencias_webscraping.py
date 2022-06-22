# %%
import os
import requests
import unicodedata
import re
import time

# %%
file_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(file_path)

# %%
os.getcwd()

# %%
#carpeta de descarga del dataset
folder_location = 'dataset_stjjalisco_sentencias'
if not os.path.exists(folder_location):os.mkdir(folder_location)
os.chdir(folder_location)
os.getcwd()

# %%
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

# %%
page_number = 0
url = "https://publica-sentencias-backend.stjjalisco.gob.mx/tocas?page=" + str(page_number) + "&sala_id=&numero=&periodo=&derivado=&delito_id=&materia_id=&nombre_delito=&accion_especifica_id=&accion_simultanea_id="
page = requests.get(url)

# %%
last_page = page.json()['data']['tocas']['last_page']
for page_number in range(0, last_page + 1):
    try:
        page = requests.get("https://publica-sentencias-backend.stjjalisco.gob.mx/tocas?page=" + str(page_number))
        if page.status_code == 429:
            time.sleep(int(page.headers['retry-after']))
        else:
            for toca in page.json()['data']['tocas']['data']:
                try:
                    print(str(toca['id']) + str("_") + str(toca['sala_id']) + str("_") + str(toca['magistrado_id']) + str("_") + str(toca["fecha_publicacion"]) + str("_") + str(toca["materia_data"]["nombre"]) + str("_") + str(toca["delito_data"]["nombre"]))
                    if toca["delito_data"]["nombre"] == 'ACCIÓN DE NULIDAD':
                    # if toca["delito_data"]["nombre"] == 'ACCIÓN DE NULIDAD' and toca["materia_data"]["nombre"] == 'Civil':
                        toca_file_response = requests.get("https://publica-sentencias-backend.stjjalisco.gob.mx/toca/" + str(toca["id"]) + "/file")
                        if toca["accion_especifica_id"] is None and toca["accion_simultanea_id"] is None:
                            toca_file_filename = 'id-' + str(toca['id']) + str('_') + 'salaid-'+ str(toca['sala_id']) + str('_') + 'magistradoid-' + str(toca['magistrado_id']) + str('_') + str(toca["fecha_publicacion"]) + str("_") + str(toca["materia_data"]["nombre"]) + str("_") + str(toca["delito_data"]["nombre"])
                        elif toca["accion_especifica_id"] is not None and toca["accion_simultanea_id"] is not None:
                            toca_file_filename = 'id-' + str(toca['id']) + str('_') + 'salaid-' + str(toca['sala_id']) + str('_') + 'magistradoid-' + str(toca['magistrado_id']) + str('_') + str(toca["fecha_publicacion"]) + str("_") + str(toca["materia_data"]["nombre"]) + str("_") + str(toca["delito_data"]["nombre"]) + str("_") + str(toca["accion_especifica_id"]['nombre']) + str("_") + str(toca["accion_simultanea_id"]['nombre'])
                        elif toca["accion_especifica_id"] is not None and toca["accion_simultanea_id"] is None:
                            toca_file_filename = 'id-' + str(toca['id']) + str('_') + 'salaid-'+ str(toca['sala_id']) + str('_') + 'magistradoid-' + str(toca['magistrado_id']) + str('_') + str(toca["fecha_publicacion"]) + str("_") + str(toca["materia_data"]["nombre"]) + str("_") + str(toca["delito_data"]["nombre"]) + str("_") + str(toca["accion_especifica_id"]['nombre'])
                        elif toca["accion_especifica_id"] is None and toca["accion_simultanea_id"] is not None:
                            toca_file_filename = 'id-' + str(toca['id']) + str('_') + 'salaid-'+ str(toca['sala_id']) + str('_') + 'magistradoid-' + str(toca['magistrado_id']) + str('_') + str(toca["fecha_publicacion"]) + str("_") + str(toca["materia_data"]["nombre"]) + str("_") + str(toca["delito_data"]["nombre"]) + str("_") + str(toca["accion_simultanea_id"]['nombre'])
                except TypeError:
                    pass
                finally:
                    with open(slugify(toca_file_filename) + '.pdf', 'wb') as f:
                        f.write(toca_file_response.content)   

    except:
        print("Connection refused by the server..")
        time.sleep(5)
        print("continue...")
        continue
# %%



