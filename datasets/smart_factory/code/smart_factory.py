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
DATASET_PATH = pathlib.Path(__file__).resolve().parent.parent
UTILS_PATH = CURRENT_PATH.parent.parent.parent
sys.path.append(str(UTILS_PATH))
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
			self.sensor = 'StencilPrinter FlowRate'
		if self.sensor_category == 'VibrationAcceleration':
			self.sensor = 'Placement Machine Vibration Z-Axis Acceleration'
		if self.sensor_category == 'Vibration':
			self.sensor = 'Placement Machine Background Vibration Z-Axis Gyroscope'
		if self.sensor_category == 'Humidity':
			self.sensor_id = self.random_item(population=['mtn-us1-svl-mp4-east1-pcba7-4ro-3-1', 'mtn-us1-svl-mp4-east1-pcba7-1sp-2-2'])
		if self.sensor_category == 'Quality':
			self.sensor_id = self.random_item(population=['mtn-us1-svl-mp4-east1-pcba7-4ro-q', 'mtn-us1-svl-mp4-east1-pcba7-2pm-q', 'mtn-us1-svl-mp4-east1-pcba7-1sp-q'])
		if self.sensor_category == 'Temperature':
			self.sensor_id = self.random_item(population=['mtn-us1-svl-mp4-east1-pcba7-4ro-3-2', 'mtn-us1-svl-mp4-east1-pcba7-1sp-2-3'])
		if self.sensor_category == 'Flow':
			self.sensor_id = 'mtn-us1-svl-mp4-east1-pcba7-1sp-2-1'
		if self.sensor_category == 'VibrationAcceleration':
			self.sensor_id = 'mtn-us1-svl-mp4-east1-pcba7-2pm-1-1'
		if self.sensor_category == 'Vibration':
			self.sensor_id = 'mtn-us1-svl-mp4-east1-pcba7-2pm-1-2'
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
equipment_out = []
@dataclasses.dataclass
class Equipment(DataUtil.DataUtil):
	id: str = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	name: str = dataclasses.field(init=False)
	type: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.name = self.random_item(population=['ReflowOven WorkCell', 'StencilPrinter WorkCell', 'PlacementMachine WorkCell'])
		if self.name == 'ReflowOven WorkCell':
			self.type = 'Cym-30-RO'
		if self.name == 'StencilPrinter WorkCell':
			self.type = 'Cym-10-SP'
		if self.name == 'PlacementMachine WorkCell':
			self.type = 'Cym-20-PM'

		equipment_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.name},{self.type}'
product_out = []
@dataclasses.dataclass
class Product(DataUtil.DataUtil):
	id: str = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	productype_id: str = dataclasses.field(init=False)
	created_at: datetime = dataclasses.field(init=False)

	def __post_init__(self):
		self.productype_id = self.random_item(population=['p-lidarcontroll-A5244-R2'])
		self.created_at = self.created_at(datetime.datetime(2022, 1, 1))

		product_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.productype_id},{self.created_at}'

if __name__ == "__main__":
  for i in range(50):
    print(Sensor_Data())
    print(Equipment())
    print(Product())
    
keys = sensor_data_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/sensor_data.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(sensor_data_out)
keys = equipment_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/equipment.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(equipment_out)
keys = product_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/product.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(product_out)
