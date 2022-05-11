import collections
import csv
import dataclasses
import datetime
import itertools
import json
import pathlib
import sys
import typing

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PARENT_PATH = CURRENT_PATH.parent.parent.parent
sys.path.append(str(PARENT_PATH))
from utils import DataUtil
import faker

fake = faker.Faker()

sensor_data_out = []
@dataclasses.dataclass
class Sensor_Data(DataUtil.DataUtil):
	created_at: datetime = dataclasses.field(init=False)
	sensor_category: str = dataclasses.field(init=False)
	sensor: str = dataclasses.field(init=False)
	sensor_id: str = dataclasses.field(init=False)
	sensor_value_unit: str = dataclasses.field(init=False)
	sensor_value: float = dataclasses.field(init=False)

	def __post_init__(self):
		self.created_at = self.created_at(datetime.datetime(2022, 1, 1))
		self.sensor_category = self.random_item(population=['Humidity', 'Quality', 'Temperature', 'Flow', 'VibrationAcceleration', 'Vibration'], distribution=[0.25, 0.02, 0.1, 0.25, 0.15, 0.15])
		if self.sensor_category == 'Humidity':
			self.sensor = self.random_item(population=['StencilPrinter Humidity', 'ReflowOven Humidity'])
		if self.sensor_category == 'Quality':
			self.sensor = self.random_item(population=['Visual Quality Inspection', 'Electronic inspection'])
		if self.sensor_category == 'Temperature':
			self.sensor = self.random_item(population=['StencilPrinter Temperature', 'ReflowOven Temperature'])
		if self.sensor_category == 'Flow':
			self.sensor = self.random_item(population=['StencilPrinter FlowRate'])
		if self.sensor_category == 'VibrationAcceleration':
			self.sensor = self.random_item(population=['Placement Machine Vibration Z-Axis Acceleration'])
		if self.sensor_category == 'Vibration':
			self.sensor = self.random_item(population=['Placement Machine Background Vibration Z-Axis Gyroscope'])
		self.sensor_value_unit = self.random_item(population=['%', 'C', 'ml/s', 'mm/s^2'], distribution=[0.3, 0.3, 0.1, 0.3])
		if self.sensor_value_unit == '%':
			self.sensor_value = self.random_float(0.27, 48)
		if self.sensor_value_unit == 'C':
			self.sensor_value = self.random_float(21, 250)
		if self.sensor_value_unit == 'ml/s':
			self.sensor_value = self.random_float(0, 0.95)
		if self.sensor_value_unit == 'mm/s^2':
			self.sensor_value = self.random_float(-16, 16)

		sensor_data_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.created_at},{self.sensor_category},{self.sensor},{self.sensor_id},{self.sensor_value_unit},{self.sensor_value}'

if __name__ == "__main__":
  for i in range(500):
    print(Sensor_Data())
    
keys = sensor_data_out[0].keys()
a_file = open(f"../output/sensor_data.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(sensor_data_out)
