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

customer_out = []
@dataclasses.dataclass
class Customer(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	accepts_marketing: str = dataclasses.field(init=False)
	created_at: datetime = dataclasses.field(init=False)
	gender: str = dataclasses.field(init=False)
	first_name: str = dataclasses.field(init=False)
	last_name: str = dataclasses.field(init=False)
	email: str = dataclasses.field(init=False)
	phone_number: str = dataclasses.field(init=False)
	tax_exempt: str = dataclasses.field(init=False)
	order_count: int = dataclasses.field(init=False)
	total_spend: float = dataclasses.field(init=False)
	country: str = dataclasses.field(init=False)
	verified_email: str = dataclasses.field(init=False)
	new_vs_repeat: str = dataclasses.field(init=False)
	state: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.accepts_marketing = self.random_item(population=['yes', 'no'], distribution=[0.2, 0.8])
		self.created_at = self.created_at(datetime.datetime(2022, 1, 1))
		self.gender = self.random_item(population=['male', 'female'], distribution=[0.5, 0.5])
		if self.gender == 'male':
			self.first_name = fake.first_name_male()
		if self.gender == 'female':
			self.first_name = fake.first_name_female()
		self.last_name = fake.last_name_nonbinary()
		self.email = f'{self.first_name.lower()}{self.last_name.lower()}@fakeshopify.com'
		self.phone_number = fake.phone_number()
		self.tax_exempt = self.random_item(population=['yes', 'no'])
		self.order_count = self.random_int(0, 10)
		if self.order_count == 0:
			self.total_spend = 0
		if 1 <= self.order_count <= 3:
			self.total_spend = self.random_float(50, 350)
		if 4 <= self.order_count <= 7:
			self.total_spend = self.random_float(325, 800)
		if 8 <= self.order_count <= 10:
			self.total_spend = self.random_float(750, 1100)
		self.country = fake.country()
		self.verified_email = self.random_item(population=['yes', 'no'])

		if self.order_count <= 1:
			self.new_vs_repeat = "new"
		else:
			self.new_vs_repeat = "repeat"

		self.state = self.random_item(population=["CA", "NY", "NJ", "OR", "TX", "MA"])
		customer_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.accepts_marketing},{self.created_at},{self.gender},{self.first_name},{self.last_name},{self.email},{self.phone_number},{self.tax_exempt},{self.order_count},{self.total_spend},{self.country},{self.verified_email}'

if __name__ == "__main__":
  for i in range(10000):
    print(Customer())

keys = customer_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/customer.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(customer_out)
