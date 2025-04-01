import functions_framework

from google.cloud import storage
import google.cloud.logging
import json
import datetime

@functions_framework.http
def get_weather(request):
    logging_client =  google.cloud.logging.Client()
    logger = logging_client.logger("get-7day-forecast-logger")
    logger.log_text(f"Logger initialized", severity="INFO")
    
    try:
        request_json = request.get_json(silent=True)
        request_args = request.args
        logger.log_text(f"Request got", severity="INFO")

        city = request_args['city']

        logger.log_text(f"SUCCESS the request is properly formatted", severity="INFO")

        storage_client = storage.Client()
        bucket = storage_client.bucket("weather-data1")
        logger.log_text(f"Got GCS bucket", severity="INFO")

        full_data = []
        current_day = datetime.date.today() + datetime.timedelta(days=1)

        for i in range(7):
            current_day_str = current_day.strftime("%Y-%m-%d")
            logger.log_text(f"Requesting current for city {city} and date {current_day_str}", severity="INFO")
            fname = f"weather_forecast_{city}_{current_day_str}.json"
            blob = bucket.blob(fname)
            data = json.loads(blob.download_as_string().decode("utf-8"))
            logger.log_text(f"Got data from bucket {data}", severity="INFO")
            current_day += datetime.timedelta(days=1)
            full_data.append(data)
        
        headers = {'Content-Type': 'application/json'}
        logger.log_text(f"SUCCESS returning data", severity="INFO")

        return json.dumps(full_data), 200, headers
    except Exception as e:
        logger.log_text(f"Error {e}", severity="ERROR")

        return '', 500

