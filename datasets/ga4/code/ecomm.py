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

users_out = []
@dataclasses.dataclass
class Users(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	created_at: datetime = dataclasses.field(init=False)
	gender: str = dataclasses.field(init=False)
	first_name: str = dataclasses.field(init=False)
	last_name: str = dataclasses.field(init=False)
	email: str = dataclasses.field(init=False)
	state: str = dataclasses.field(init=False)
	street_address: str = dataclasses.field(init=False)
	postal_code: str = dataclasses.field(init=False)
	city: str = dataclasses.field(init=False)
	country: str = dataclasses.field(init=False)
	latitude: float = dataclasses.field(init=False)
	longitude: float = dataclasses.field(init=False)
	traffic_source: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.created_at = self.created_at(datetime.datetime(2021, 1, 1))
		self.gender = self.random_item(population=['male', 'female'], distribution=[0.5, 0.5])
		if self.gender == 'male':
			self.first_name = fake.first_name_male()
		if self.gender == 'female':
			self.first_name = fake.first_name_female()
		self.last_name = fake.last_name_nonbinary()
		self.email = f'{self.first_name.lower()}{self.last_name.lower()}@westsidewontons.com'
		self.traffic_source = self.random_item(population=['Organic', 'Facebook', 'Search', 'Email', 'Display'], distribution=[0.2, 0.2, 0.2, 0.2, 0.2])

		users_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.created_at},{self.gender},{self.first_name},{self.last_name},{self.email},{self.state},{self.street_address},{self.postal_code},{self.city},{self.country},{self.latitude},{self.longitude},{self.traffic_source}'
orders_out = []
@dataclasses.dataclass
class Orders(DataUtil.DataUtil):
	id: int = dataclasses.field(init=False)
	user_id: int = dataclasses.field(init=False)
	status: str = dataclasses.field(init=False)
	created_at: datetime = dataclasses.field(init=False)
	returned_at: datetime = dataclasses.field(init=False)
	shipped_at: datetime = dataclasses.field(init=False)
	delivered_at: datetime = dataclasses.field(init=False)
	num_of_item: int = dataclasses.field(init=False)

	user:dataclasses.InitVar[typing.Any] = None
	def __post_init__(self, user=None):
		self.user_id == user.id
		self.status = self.random_item(population=['Complete', 'Cancelled', 'Returned'], distribution=[0.85, 0.05, 0.1])
		self.created_at = self.created_at(datetime.datetime(2021, 1, 1))
		self.num_of_item = self.random_item(population=[1, 2, 3, 4], distribution=[0.7, 0.2, 0.05, 0.05])

		orders_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.user_id},{self.status},{self.created_at},{self.returned_at},{self.shipped_at},{self.delivered_at},{self.num_of_item}'

if __name__ == "__main__":
  for i in range(10):
    print(Users())
    print(Orders())
    
keys = users_out[0].keys()
a_file = open(f"../output/users.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(users_out)
keys = orders_out[0].keys()
a_file = open(f"../output/orders.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(orders_out)
