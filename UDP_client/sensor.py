import random

class Sensor:
    def __init__(self, _type):
        if _type == 1:
            self.sensor_type = "T"
            self.sensor_value = random.randint(-10, 40)
            self.einheit = "° C"
        elif _type == 2:
            self.sensor_type = "H"
            self.sensor_value = random.randint(50, 75)
            self.einheit = "%"
        elif _type == 3:
            self.sensor_type = "LI"
            self.sensor_value = random.randint(100, 4000)
            self.einheit = "lm"

    def get_sensor_value(self):
        if(self.sensor_type == "T"):
            interval = random.randint(0, 3)
            return self.sensor_value - interval
        elif(self.sensor_type == "H"):
            interval = random.randint(0, 3)
            return self.sensor_value - interval
        elif(self.sensor_type == "LI"):
            interval = random.randint(0, 5)
            return self.sensor_value - interval
    
    def get_sensor_type(self):
        return self.sensor_type
    
    def get_sensor_unit(self):
      return self.einheit