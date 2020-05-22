from abc import ABC, abstractmethod

class Sensor(ABC):
"""
    Abstract class for sensors, to ensure they all provide the standard functions
"""

    def __init__(self, name, logging_interval):
        """
            Initialises the sensor with its name and logging interval (in minutes)
        """
        self.name = name
        self.logging_interval = logging_interval

    @abstractmethod
    def take_reading(self):
        raise NotImplementedError




class TemperatureSensor(Sensor):

    def __init__(self, name, logging_interval):
        super().__init__(name, logging_interval)

    def take_reading(self):
        pass
