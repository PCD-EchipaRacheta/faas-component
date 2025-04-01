import functions_framework

from google.cloud import storage
import google.cloud.logging
import json

from datetime import date

@functions_framework.http
def get_weather(request):
    logging_client =  google.cloud.logging.Client()
    logger = logging_client.logger("get-daily-weather-logger")
    logger.log_text(f"Logger initialized", severity="INFO")
    
    try:
        request_json = request.get_json(silent=True)
        request_args = request.args
        logger.log_text(f"Request got", severity="INFO")

        city = request_args['city']
        today = date.today().strftime("%Y-%m-%d")
        logger.log_text(f"Requesting current for city {city} and date {today}", severity="INFO")
        logger.log_text(f"SUCCESS the request is properly formatted", severity="INFO")
        fname = f"weather_forecast_{city}_{today}.json"

        storage_client = storage.Client()
        bucket = storage_client.bucket("weather-data1")
        logger.log_text(f"Got GCS bucket", severity="INFO")
        blob = bucket.blob(fname)
        data = blob.download_as_string().decode("utf-8")
        logger.log_text(f"Got data from bucket {data}", severity="INFO")
        headers = {'Content-Type': 'application/json'}
        logger.log_text(f"SUCCESS returning data", severity="INFO")

        return data, 200, headers
    except Exception as e:
        logger.log_text(f"Error {e}", severity="ERROR")

        return '', 500

