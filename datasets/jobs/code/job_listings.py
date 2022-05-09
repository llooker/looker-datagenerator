import collections
import csv
import dataclasses
import datetime
import itertools
import json
import typing

from utils import DataUtil
import faker
fake = faker.Faker()

jobs_out = []
@dataclasses.dataclass
class Jobs(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	level: int = dataclasses.field(init=False)
	org: str = dataclasses.field(init=False)
	title: str = dataclasses.field(init=False)

	def __post_init__(self):
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

		jobs_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.level},{self.org},{self.title}'

if __name__ == "__main__":
  for i in range(100):
    print(Jobs())
    
keys = jobs_out[0].keys()
a_file = open(f"data/jobs.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(jobs_out)
