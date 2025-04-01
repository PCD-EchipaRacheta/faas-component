import functions_framework

warning_levels = {
    "Heat - Yellow": range(35, 38),
    "Heat - Orange": range(38, 40),
    "Heat - Red": [40],
    "Cold - Yellow": range(-18, -14),
    "Cold - Orange": range(-22, -20),
    "Cold - Red": [-23]
}


def get_temp_warning(temp):
    for level, values in warning_levels.items():
        if temp in values:
            return level
    return "No warning"


@functions_framework.http
def notify_temp(request):
    req = request.get_json()
    city = req.get("city")
    try:
        temperature = float(req.get("temperature"))
    except (TypeError, ValueError):
        return "Invalid temperature", 400

    if not city:
        return "Invalid city", 400

    level = get_temp_warning(temperature)
    message = f"Temperature in {city} is {temperature}°C. "

    if level == "Heat - Yellow":
        message += "Heat Watch!"
    elif level == "Heat - Orange":
        message += "Heat Warning!"
    elif level == "Heat - Red":
        message += "Extreme Heat Warning!"
    elif level == "Cold - Yellow":
        message += "Cold Watch!"
    elif level == "Cold - Orange":
        message += "Cold Warning!"
    elif level == "Cold - Red":
        message += "Extreme Cold Warning!"
    else:
        message += "Normal temperature."

    return message, 200
