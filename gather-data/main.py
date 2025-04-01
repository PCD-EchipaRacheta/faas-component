import functions_framework


import requests
import json

from google.cloud import storage
from google.cloud import secretmanager
import google.cloud.logging

def access_secret_weatherAPIKey():
    secret_client = secretmanager.SecretManagerServiceClient()
    name = f"projects/41335490407/secrets/weatherAPI-key/versions/latest"      
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def upload_to_gcs(fname, data):
    storage_client = storage.Client()
    bucket = storage_client.bucket("weather-data1")
    blob = bucket.blob(fname)
    
    blob.upload_from_string(data, content_type="application/json")


def get_weather_forecast():

    try:
        logging_client =  google.cloud.logging.Client()
        logger = logging_client.logger("gather-data-logger")
        # 
        logger.log_text("Before checking secret manager for API Key", severity="INFO")
        API_key = access_secret_weatherAPIKey()
        logger.log_text("SUCCESS checking secret manager for API Key", severity="INFO")
        
        CITIES = ["Iasi", "Bucharest", "Cluj-Napoca", "Timisoara", "Constanta", "Craiova", "Brasov", "Ploiesti", "Suceava", "Galati"]
        
        for city in CITIES:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={API_key}&q={city}&days=0&aqi=no&alerts=yes"
            response = requests.get(url)
            response.raise_for_status()
            logger.log_text(f"SUCCESS gather data from weather service for {city}", severity="INFO")
            data = response.json()
            
            fname = f"weather_data_{city}_current.json"
            current_data = json.dumps(data['current'])
            upload_to_gcs(fname, current_data)
            logger.log_text("SUCCESS uploading to GCS", severity="INFO")
    except Exception as e:
        logger.log_text(f"{e}", severity="ERROR")
        return '', 500


@functions_framework.http
def gather_date_and_push_to_gcs(request):

    get_weather_forecast()

    return '', 200
