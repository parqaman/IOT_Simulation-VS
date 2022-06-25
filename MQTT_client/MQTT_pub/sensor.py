import random

class Sensor:
    def __init__(self, _type):
        if _type == 1:
            self.sensor_type = "T"
            self.sensor_value = random.randint(50, 100)
            self.einheit = "Fahr"
        elif _type == 2:
            self.sensor_type = "WQ"
            self.sensor_value = random.randint(0, 7)
            self.einheit = "pH"
        elif _type == 3:
            self.sensor_type = "AQ"
            self.sensor_value = random.randint(100, 150)
            self.einheit = "US"

    def get_sensor_value(self):
        if(self.sensor_type == "T"):
            interval = random.randint(0, 5)
            return self.sensor_value - interval
        elif(self.sensor_type == "WQ"):
            interval = random.randint(0, 1)
            return self.sensor_value - interval
        elif(self.sensor_type == "AQ"):
            interval = random.randint(0, 7)
            return self.sensor_value - interval
    
    def get_sensor_type(self):
        return self.sensor_type
    
    def get_sensor_unit(self):
      return self.einheit