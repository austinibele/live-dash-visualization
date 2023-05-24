from flask import Flask
import random
import json
from datetime import datetime

app = Flask(__name__)

N_SENSORS = 9
TEMPERATURE = 80

# Set the starting temperature for each sensor
temperatures = [TEMPERATURE for _ in range(N_SENSORS)]

def update_temperature(old_temp):
    # Choose a random amount to change the temperature, with a maximum change of 0.05
    change = random.uniform(-0.05, 0.05)

    # Update the temperature and ensure it stays within the 149.75 - 150.25 range
    new_temp = old_temp + change
    new_temp = max(79.75, min(80.25, new_temp))

    return new_temp

@app.route('/', methods=['GET'])
def get_temperature():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    # Update each sensor's temperature
    global temperatures
    temperatures = [update_temperature(t) for t in temperatures]

    # Check that the maximum temperature difference is less than 1 degree
    if max(temperatures) - min(temperatures) >= 1:
        temperatures = [t - 0.05 for t in temperatures] if max(temperatures) > TEMPERATURE else [t + 0.05 for t in temperatures]
    
    payload = {"time": formatted_datetime, "num_sensors": f"{N_SENSORS}", "temperatures": [str(round(t, 2)) for t in temperatures]}
    
    return json.loads(json.dumps(payload))

if __name__ == "__main__":
    app.run(debug=False)
