# [START functions]
from cloudevents.http import CloudEvent
from google.cloud import storage
from google.cloud import bigquery
import functions_framework
#
import os
import requests
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

# Realizar la solicitud HTTP
def request_yelp(api_key, table_id, params):    
    url = f"https://api.yelp.com/v3/{table_id}/search?{params}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Normalizar la respuesta JSON y convertirla en un data frame
def normalize(json_response, table_id):
    # seleccionar la columna "businesses"
    businesses = json_response[table_id]    
    # Convertir el objeto JSON en un DataFrame de pandas
    df = pd.json_normalize(businesses)
    # Renombrar las columnas
    df = df.rename(columns={"id": "business_id"})
    df = df.rename(columns={"rating": "stars"})
    df = df.rename(columns={"coordinates.latitude": "latitude"})
    df = df.rename(columns={"coordinates.longitude": "longitude"})
    df = df.rename(columns={"location.address1": "address1"})
    df = df.rename(columns={"location.address2": "address2"})
    df = df.rename(columns={"location.address3": "address3"})
    df = df.rename(columns={"location.city": "city"})
    df = df.rename(columns={"location.zip_code": "postal_code"})
    df = df.rename(columns={"location.country": "country"})
    df = df.rename(columns={"location.state": "state"})
    df = df.rename(columns={"location.display_address": "address"})    
    # Convertir is_closed a is_open invirtiendo el valor    
    df["is_closed"] = df["is_closed"].apply(lambda x: 0 if x else 1)
    df = df.rename(columns={"is_closed": "is_open"})
    # Extraer valor de title de categories y guardar un string separado por comas
    df["categories"] = df["categories"].apply(lambda x: ", ".join([y["title"] for y in x]))
    # Convertir address en string separado por espacios
    df["address"] = df["address"].apply(lambda x: " ".join(x))
    # Crear columna date #TODO: obtener de check-in
    df["date"] = "2013-01-05 14:52:30, 2013-01-19 14:21:37, 2013-04-10 01:18:43, 2013-04-13 14:40:13, 2013-10-02 23:06:36, 2013-10-30 22:13:59, 2013-11-06 23:58:42, 2015-08-14 22:12:45"
    # Seleccionar las columnas que se van a usar
    fields = ["business_id", "date", "name", "address", "city", "state", "postal_code", "latitude", "longitude", "stars", "review_count", "is_open", "categories"]
    df = df[fields]
    # df = df[df["categories"].str.contains(category, case=False, na=False)]
    return df

# Guardar un data frame en GCS
def df_to_bq(df, destination_table, project_id):
    """
    Guarda un dataframe de pandas en BigQuery
    """
    # convertir a string
    df = df.astype(str)
    # guardar en BigQuery
    df.to_gbq(destination_table=destination_table, project_id=project_id, if_exists="replace")

# Función de entrada
@functions_framework.http
def main(request):
    # CONSTANTES
    GCP_PROJECT = os.environ.get("GCP_PROJECT")    
    YELP_API_KEY = os.environ.get("YELP_API_KEY")
    TABLE_ID = "businesses"
    DATASET_ID = "astoria"

    # Selecciono la categoría en Yelp que seo buscar y analizar
    category = "recreation"
    # Cargar la respuesta JSON en un objeto Python
    params = f"categories={category}&location=FL&sort_by=best_match"
    # Realizar la solicitud HTTP
    data = request_yelp(YELP_API_KEY, TABLE_ID, params)
    # Normalizar la respuesta JSON y convertirla en un dataframe
    df = normalize(data, TABLE_ID)

    # tabla de destino
    destination_table = f"{DATASET_ID}.Yelp_Checkin_Business_TBL"
    df_to_bq(df, destination_table, GCP_PROJECT)

    # Return an HTTP response
    return "OK"

# [END functions]
