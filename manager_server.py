from flask import Flask
from flask import request, jsonify
import csv, os
from datetime import datetime

LOG_FILE = 'sensor_log.csv'

if not os.path.exists(LOG_FILE):
   with open(LOG_FILE, 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(['timestamp', 'id_device', 'sensor_type', 'flow', 'volume'])

app = Flask("__server_manager__")

@app.route('/sensor/dump/<devname>', methods=['GET'])

def end_point_GET(devname):
    with open(LOG_FILE, 'r', newline='') as f:
        dizionario = csv.DictReader(f)
        results = []
        for row in dizionario:
            if row['id_device'] == devname:
                results.append(row)

    return results

@app.route('/sensor/water_network', methods=['POST'])

def prelievo_dati():
    data = request.get_json()
    print(data)
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['timestamp'], data['id_device'], data['sensor_type'], data['flow'], data['volume']])

    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)