from utils import DataUtil  
import dataclasses
from dataclasses import field
import itertools
import datetime
import faker
fake = faker.Faker()

@dataclasses.dataclass
class Employees(DataUtil):
	id: int = field(default_factory=itertools.count(start=1).__next__)
	gender: str = field(init=False)
	first_name: str = field(init=False)
	last_name: str = field(init=False)
	email: str = field(init=False)
	level: int = field(init=False)
	role: str = field(init=False)

	def __post_init__(self):
		self.gender = self.random_item(population=['male', 'female', 'nonbinary'], distribution=[0.4, 0.5, 0.1])
		if self.gender == 'male':
			self.first_name = fake.first_name_male()
		if self.gender == 'female':
			self.first_name = fake.first_name_female()
		if self.gender == 'nonbinary':
			self.first_name = fake.first_name_nonbinary()
		self.last_name = fake.last_name_nonbinary()
		self.email = f'{self.first_name.lower()}{self.last_name.lower()}@testco.com'
		self.level == self.random_int(1, 5)
		self.role = self.random_item(population=['account executive', 'sales engineer', 'customer success analyst', 'engineer', 'recruiter'], distribution=[0.6, 0.1, 0.1, 0.1, 0.1])

		def __str__(self):
			return f'{self.id},{self.gender},{self.first_name},{self.last_name},{self.email},{self.level},{self.role}'

if __name__ == "__main__":
  for i in range(100):
    print(Employees())