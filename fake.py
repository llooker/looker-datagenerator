import collections
import csv
import dataclasses
import datetime
import itertools
import json

from utils import DataUtil
import faker
fake = faker.Faker()
employees_out = []
@dataclasses.dataclass
class Employees(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	gender: str = dataclasses.field(init=False)
	first_name: str = dataclasses.field(init=False)
	last_name: str = dataclasses.field(init=False)
	hired_date: datetime = dataclasses.field(init=False)
	email: str = dataclasses.field(init=False)
	level: int = dataclasses.field(init=False)
	org: str = dataclasses.field(init=False)
	title: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.gender = self.random_item(population=['male', 'female', 'nonbinary'], distribution=[0.4, 0.5, 0.1])
		if self.gender == 'male':
			self.first_name = fake.first_name_male()
		if self.gender == 'female':
			self.first_name = fake.first_name_female()
		if self.gender == 'nonbinary':
			self.first_name = fake.first_name_nonbinary()
		self.last_name = fake.last_name_nonbinary()
		self.hired_date = self.created_at(datetime.datetime(2015, 1, 1))
		self.email = f'{self.first_name.lower()}{self.last_name.lower()}@testco.com'
		self.level = self.random_int(1, 5)
		self.org = self.random_item(population=['Sales', 'Marketing', 'Engineering', 'Product', 'Customer Success'])
		if self.org == 'Sales':
			self.title = self.random_item(population=['AE', 'SE', 'FSR'])
		if self.org == 'Marketing':
			self.title = self.random_item(population=['Marketing Analyst', 'Marketing Manager'])
		if self.org == 'Engineering':
			self.title = self.random_item(population=['SWE', 'Data Eng'])
		if self.org == 'Product':
			self.title = self.random_item(population=['PM', 'UI', 'UX'])
		if self.org == 'Customer Success':
			self.title = self.random_item(population=['CSM', 'CSE', 'TSM'])

		employees_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.gender},{self.first_name},{self.last_name},{self.hired_date},{self.email},{self.level},{self.org},{self.title}'

if __name__ == "__main__":
  for i in range(100):
    print(Employees())
    
keys = employees_out[0].keys()
a_file = open(f"data/employees.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(employees_out)
