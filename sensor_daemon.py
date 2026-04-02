import csv
import time
import sys
import requests

def data_to_mgrSvr():
    FILE = 'consumi_idrici_universita.csv'

    id_sensor = sys.argv[1]
    with open(FILE, 'r', newline='') as f:
        dict = csv.DictReader(f)
        for row in dict:
            if row['id_sensor'] == id_sensor:
                requests.post('http://192.168.1.1:5000/sensor/water_network', 
                              json={'id_device': row['id_sensor'], 
                                    'sensor_type': 'water', 
                                    'flow': row['flow'], 
                                    'volume': row['volume']})
                time.sleep(1)


if __name__ == '__main__':
    data_to_mgrSvr()