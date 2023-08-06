from heightsensor import Sensor


sensor = Sensor()
sensor.connect()

print(sensor.read(4096))
