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

comments_out = []
@dataclasses.dataclass
class Comments(DataUtil.DataUtil):
	url: str = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	source_system: str = dataclasses.field(init=False)
	created_at: datetime = dataclasses.field(init=False)
	comment_text: str = dataclasses.field(init=False)
	user_name: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.source_system = self.random_item(population=['GMB', 'YT'])
		self.created_at = self.created_at(datetime.datetime(2022, 1, 1))
		self.comment_text = fake.sentence(nb_words=10)
		self.user_name = fake.user_name()
		comments_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.url},{self.source_system},{self.created_at},{self.comment_text},{self.user_name}'
products_out = []
@dataclasses.dataclass
class Products(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	description: str = dataclasses.field(init=False)
	channel: str = dataclasses.field(init=False)
	availability: str = dataclasses.field(init=False)
	price: float = dataclasses.field(init=False)
	gtin: str = dataclasses.field(init=False)
	google_product_category_path: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.description = fake.sentence(nb_words=5)
		self.channel = self.random_item(population=['online', 'local'])
		self.availability = self.random_item(population=['Available', 'Unavailable', 'In-Transit'], distribution=[0.5, 0.3, 0.2])
		self.price = self.random_int(0, 100)
		self.gtin = fake.bothify('#' * 12)
		self.google_product_category_path = fake.uri_path()
		products_out.append(dataclasses.asdict(self))
		inventory_out.append(dataclasses.asdict(Inventory(products=self)))
	def __str__(self):
		return f'{self.id},{self.description},{self.channel},{self.availability},{self.price},{self.gtin},{self.google_product_category_path}'
inventory_out = []
@dataclasses.dataclass
class Inventory(DataUtil.DataUtil):
	product_id: str = dataclasses.field(init=False)
	# store_code: str = dataclasses.field(init=False)
	availability: str = dataclasses.field(init=False)
	quantity: int = dataclasses.field(init=False)

	products:dataclasses.InitVar[typing.Any] = None
	stores:dataclasses.InitVar[typing.Any] = None
	def __post_init__(self, products=None, stores=None):
		print(products.id)
		self.product_id = products.id
		# self.store_code = stores.store_code
		self.availability = self.random_item(population=['available', 'out of stock'])
		self.quantity = self.random_int(0, 5)

		inventory_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.product_id},{self.store_code},{self.availability},{self.quantity}'
stores_out = []
@dataclasses.dataclass
class Stores(DataUtil.DataUtil):
	store_code: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	store_name: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.store_name = self.random_item(population=['store1', 'store2', 'store3', 'store4', 'store4', 'store5', 'store6', 'store7', 'store8', 'store9', 'store10'])

		stores_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.store_code},{self.store_name}'
customers_out = []
@dataclasses.dataclass
class Customers(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	gender: str = dataclasses.field(init=False)
	first_name: str = dataclasses.field(init=False)
	last_name: str = dataclasses.field(init=False)
	loyalty_tier: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.gender = self.random_item(population=['male', 'female', 'nonbinary'])
		if self.gender == 'male':
			self.first_name = fake.first_name_male()
		if self.gender == 'female':
			self.first_name = fake.first_name_female()
		if self.gender == 'nonbinary':
			self.first_name = fake.first_name_nonbinary()
		self.last_name = fake.last_name_nonbinary()
		self.loyalty_tier = self.random_item(population=['gold', 'silver', 'bronze'])

		customers_out.append(dataclasses.asdict(self))
		transactions_out.append(dataclasses.asdict(Transactions(customers=self)))
	def __str__(self):
		return f'{self.id},{self.gender},{self.first_name},{self.last_name},{self.loyalty_tier}'
transactions_out = []
@dataclasses.dataclass
class Transactions(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	customer_id: int = dataclasses.field(init=False)
	product_id: int = dataclasses.field(init=False)
	cost: float = dataclasses.field(init=False)

	customers:dataclasses.InitVar[typing.Any] = None
	# products:dataclasses.InitVar[typing.Any] = None
	def __post_init__(self, customers=None, products=None):
		self.customer_id = customers.id
		self.product_id = logic_to_determine_product()
		self.cost = self.random_int(0, 100)

		transactions_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.customer_id},{self.product_id},{self.cost}'



if __name__ == "__main__":
  for i in range(100):
    print(Comments())
    print(Products())
    # print(Inventory())
    print(Stores())
    print(Customers())
    # print(Transactions())

keys = comments_out[0].keys()
a_file = open(f"data/comments.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(comments_out)
keys = products_out[0].keys()
a_file = open(f"data/products.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(products_out)
keys = inventory_out[0].keys()
a_file = open(f"data/inventory.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(inventory_out)
keys = stores_out[0].keys()
a_file = open(f"data/stores.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(stores_out)
keys = customers_out[0].keys()
a_file = open(f"data/customers.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(customers_out)
keys = transactions_out[0].keys()
a_file = open(f"data/transactions.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(transactions_out)
