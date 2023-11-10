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

API_KEY = os.environ.get("GMAPS_API_KEY")

# Realizar la solicitud HTTP
def request_api(url, params):    
    url = f"{url}?{params}&key={API_KEY}"
    response = requests.get(url)
    return response.json()

# Obtener localización de un estado
def get_state_metadata(state):
    url="https://maps.googleapis.com/maps/api/geocode/json"
    params=f"address={state}"
    response_json = request_api(url, params)
    result = response_json["results"][0]
    return result

# Obtener lugares cercanos
def get_nearby_places(location, radius=50000, place_type="business"):
    url="https://maps.googleapis.com/maps/api/place/nearbysearch/json"    
    # fields = "place_id,rating,user_ratings_total"
    params=f"location={location}&radius={radius}&type={place_type}"#&fields={fields}"
    places_response = request_api(url, params)
    result = places_response["results"]
    return result

# Obtener detalles de un lugar
def get_place_details(place_id):    
    fields = "name,formatted_address,place_id,geometry,types"
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params= f"place_id={place_id}&fields={fields}"
    response_json = request_api(url, params)
    print(response_json)
    result = response_json["result"]
    return result

# Normalizar los datos
# Normalizar los datos
def normalize(places):
    parsed_places = []
    for place in places:
        place["address"] = place["vicinity"]
        place["gmap_id"] = place["place_id"]
        place["description"] = ""
        place["latitude"] = place["geometry"]["location"]["lat"]
        place["longitude"] = place["geometry"]["location"]["lng"]
        place["category"] = place["types"]
        place["avg_rating"] = place.get("rating", 0)
        place["num_of_reviews"] = place.get("user_ratings_total", 0)
        place["price"] = place.get("price_level", 0)
        place["hours"] = ""
        place["state"] = "Florida"
        place["url"] = "https://www.google.com/maps/place//data="+place["place_id"]        
        parsed_places.append(place)
    fields = ["name", "address", "gmap_id", "description", "latitude", "longitude", "category", "avg_rating", "num_of_reviews", "price", "hours", "state", "url"]
    df = pd.DataFrame(parsed_places, columns=fields)
    df["category"] = df["category"].apply(lambda x: " ".join(x))
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
    DATASET_ID = "astoria"
    # obtener datos de la API
    geocoding = get_state_metadata("Florida")
    location = f"{geocoding['geometry']['location']['lat']},{geocoding['geometry']['location']['lng']}"    
    places = get_nearby_places(location)
    df = normalize(places)
    # tabla de destino
    destination_table = f"{DATASET_ID}.Meta_Data_TBL"
    df_to_bq(df, destination_table, GCP_PROJECT)

    # Return an HTTP response
    return "OK"

# [END functions]
