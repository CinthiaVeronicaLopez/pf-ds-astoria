# [START functions_cloudevent_storage]
from cloudevents.http import CloudEvent
from google.cloud import storage
from google.cloud import bigquery
import functions_framework
#
import pandas as pd
import json
import os

# Normalizar Categorías
def normalize_categories(category_list):
    '''
    Normaliza la lista de categorías
    '''
    if category_list is not None:
        return [category.strip() for category in category_list]
    else:
        return None

# Normalizar Horas
def normalize_hours(hours_list):
    '''
    Normaliza la lista de horas
    '''
    if hours_list is not None:
        normalized_hours = []
        for day_hours in hours_list:
            if len(day_hours) == 2:
                day, hours = day_hours
                normalized_day_hours = f"{day}: {hours}"
                normalized_hours.append(normalized_day_hours)
        return normalized_hours
    else:
        return None

# Normalizar Json
def normalize(j):
    '''
    Normaliza el json
    '''
    fields = ['name', 'address', 'gmap_id', 'description', 'latitude', 'longitude', 'category', 'avg_rating', 'num_of_reviews', 'price', 'hours', 'state', 'url']
    df = pd.DataFrame(j, columns=fields)
    df['category'] = df['category'].apply(normalize_categories)
    df_meta = df.dropna(subset=['category'])
    df_meta = df_meta.explode('category')
    # df_meta = df_meta.drop(columns=['relative_results'])
    # df_meta = df_meta.drop(columns=['MISC'])
    df_meta['hours'] = df_meta['hours'].apply(normalize_hours)
    df_meta['hours'] = df_meta['hours'].apply(lambda x: ', '.join(x) if x is not None else None)
    return df_meta

#
def read_json_from_gcs(bucket_name, file_name):
    '''
    Lee un json de GCS
    '''
    print("read_json_from_gcs")
    # Inicializar el cliente de GCS
    client = storage.Client()
    # Obtiene el bucket de GCS
    bucket = client.get_bucket(bucket_name)
    try:
        # leer el archivo 
        blob = bucket.get_blob(file_name)
    except Exception as e:
        print(f"An error occurred: {e}")

    return blob

#
def df_to_bq(df, project_id, dataset_id, table_id):
    '''
    Guarda un dataframe de pandas en BigQuery
    '''
    print("df_to_bq")
    # Crear el cliente de BigQuery
    client = bigquery.Client()
    destination_table = f"{dataset_id}.{table_id}"
    # Guardar el dataframe en BigQuery
    df.to_gbq(destination_table=destination_table, project_id=project_id, 
    if_exists='replace')

# Procesamiento por lotes
def batch_process(project_id, dataset_id, table_id, category_selected, blob):
    '''
    Procesa un archivo json de GCS en lotes
    '''
    print("batch_process")
    result = ''
    # Tamaño del lote
    batch_size = 1
    # Inicializar un DataFrame vacío para almacenar el lote actual
    batch_df = pd.DataFrame()
    # Contador para llevar un registro del tamaño del lote actual
    counter = 0
    # leer el archivo json linea por linea y ejecutar la función normalize
    stream = blob.open("rt")
    # for line in blob.download_as_string().decode("utf-8").splitlines():
    for line in stream:
        # Lee el archivo JSON
        j = json.loads(line)
        normalized = normalize([j])
        # Seleccionar solo las atracciones turísticas
        print(f"Seleccionar solo las atracciones turísticas")
        normalized = normalized[normalized['category'].str.contains(category_selected, case=False, na=False)]
        # Concatenar el json normalizado al dataframe del lote
        print(f"concatenar el json normalizado al dataframe del lote")
        batch_df = pd.concat([batch_df, normalized])
        counter += 1
        print(f"Procesando {counter} registros")
        # Si el tamaño del lote alcanza el tamaño del lote definido, procesa el lote y vacía el DataFrame del lote
        if counter >= batch_size:
            print(f"Si el tamaño del lote alcanza el tamaño del lote definido, procesa el lote y vacía el DataFrame del lote")
            df_to_bq(batch_df, project_id, dataset_id, table_id)
            batch_df = pd.DataFrame()
            counter = 0
    # Procesa el último lote si contiene datos
    if not batch_df.empty:
        print(f"Procesa el último lote si contiene datos")
        df_to_bq(batch_df, project_id, dataset_id, table_id)
    
    stream.close()

# Función disparada por un cambio en un bucket de almacenamiento
@functions_framework.cloud_event
def main_gcs(cloud_event: CloudEvent) -> tuple:
    '''
    Dispara la función cuando se sube un archivo a un bucket de GCS    
    '''
    print("main_gcs")
    # Obtener los datos del evento
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]
    # Obtener las variables de entorno
    project_id = os.environ.get('GCP_PROJECT')
    dataset_id = 'astoria'
    table_id = 'metadata-sites'

    category_selected = 'Tourist attraction'
    # Leer el json de GCS
    print(f"Leer {file_name} de {bucket_name}")
    blob = read_json_from_gcs(bucket_name, file_name)    
    # leer el archivo json linea por linea y ejecutar la función normalize
    print(f"Procesando...")
    batch_process(project_id, dataset_id, table_id, category_selected, blob)
    
    return 'OK', 200

# [END functions_cloudevent_storage]
