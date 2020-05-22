""" The main client class """
import json
from sensor import TemperatureSensor

class BrewClient:
    
    def __init__(self):
        # Load the settings
        with open('./data/config.json', 'r') as config_file:
            config = json.load(config_file)
            self.server_settings = config['server_settings']
            self.client_settings = config['client_settings']

        self.init_sensors()

    def init_sensors(self):
        self.sensors = []
        for sensor_settings in client_settings['sensors']:
            if sensor_settings['type'] == 'temp':
                sensor = TemperatureSensor(sensor_settings['name'],sensor_settings['logging_interval'])
            self.sensors.append(sensor)

