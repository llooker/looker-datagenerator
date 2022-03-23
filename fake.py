from utils.DataUtil import DataUtil
from faker import Faker

import dataclasses
import itertools
import json

fake = Faker()

scooters_out = []
@dataclasses.dataclass
class Scooters(DataUtil):
    id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
    model: str = dataclasses.field(init=False)
    last_battery: int = dataclasses.field(init=False)
    days_since_last_service: int = dataclasses.field(init=False)
    status: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.model = self.random_item(['Xiaomi M365', 'Ninebot-Segway ES2', 'Bespoke Scooters', 'Xiaomi 1S', 'Ninebot-Segway ES4'])
        self.last_battery = self.random_int(100)
        self.days_since_last_service = self.random_int(35)
        self.status = self.random_item(['In-Use', 'Parked: Available', 'Parked: Needs Service', 'Charging', 'In-Service', 'Unknown'])
        scooters_out.append(dataclasses.asdict(self))

    def __str__(self):
        return f"{self.id}, {self.model}, {self.last_battery}, {self.days_since_last_service}, {self.status}"


technicians_out = []
@dataclasses.dataclass
class Technicians(DataUtil):
    id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
    first_name: str = dataclasses.field(init=False)
    last_name: str = dataclasses.field(init=False)
    phone_number: str = dataclasses.field(init=False)
    email: str = dataclasses.field(init=False)
    status: str = dataclasses.field(init=False)
    level: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.phone_number = fake.unique.phone_number()
        self.email = self.first_name[0] + self.last_name + "@scooty.com"
        self.status = self.random_item(['Available', 'Utilized', 'Not working'])
        self.level = self.random_item([1, 2])
        technicians_out.append(dataclasses.asdict(self))

    def __str__(self):
        return f"{self.id}, {self.first_name}, {self.last_name}, {self.phone_number}, {self.email}, {self.status}, {self.level}"

if __name__ == "__main__":
    for i in range(100):
        print(Scooters())
        print(Technicians())
        

