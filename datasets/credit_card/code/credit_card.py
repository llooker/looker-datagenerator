import collections
import csv
import dataclasses
import datetime
import itertools
import json
import pathlib
import pandas as pd
import sys
import typing
import random

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
DATASET_PATH = pathlib.Path(__file__).resolve().parent.parent
UTILS_PATH = CURRENT_PATH.parent.parent.parent
sys.path.append(str(UTILS_PATH))
from utils import DataUtil
import faker

fake = faker.Faker()

####Static Datasets
stores = pd.read_csv(f"{DATASET_PATH}/output/store.csv").to_dict('records')
card_types = pd.read_csv(f"{DATASET_PATH}/output/card_types.csv").to_dict('records')
events_dict = pd.read_csv(f"{DATASET_PATH}/output/events.csv").to_dict('records')
transaction_types = pd.read_csv(f"{DATASET_PATH}/output/store.csv").to_dict('records')


token_out = []
@dataclasses.dataclass
class Token(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	token: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.token = fake.credit_card_number()
		token_out.append(dataclasses.asdict(self))
		random_num_tx = random.randrange(1, 10)
		for i in range(random_num_tx):
			transactions_out.append(dataclasses.asdict(Transactions(token=self)))

	def __str__(self):
		return f'{self.id},{self.token}'
transactions_out = []
@dataclasses.dataclass
class Transactions(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	token_id: int = dataclasses.field(init=False)
	date: datetime.date = dataclasses.field(init=False)
	time: datetime.time = dataclasses.field(init=False)
	terminal_id: int = dataclasses.field(init=False)
	transaction_type_id: int = dataclasses.field(init=False)
	amount: float = dataclasses.field(init=False)

	token:dataclasses.InitVar[typing.Any] = None
	terminal:dataclasses.InitVar[typing.Any] = None
	transaction_type:dataclasses.InitVar[typing.Any] = None
	def __post_init__(self, token=None, terminal=None, transaction_type=None):
		self.token_id = token.id
		self.date = self.created_at(datetime.datetime(2022, 1, 1))
		t = datetime.datetime.now()
		self.time = t.time()
		self.terminal_id = random.randrange(1, 20)
		random_transaction_type = transaction_types[random.randrange(len(transaction_types))]
		self.transaction_type_id = random_transaction_type["id"]
		self.amount = self.random_float(20, 1000)

		random_txn_events = random.randrange(3, 6)
		for i in range(random_txn_events):
			transaction_history_out.append(dataclasses.asdict(Transaction_History(transactions = self)))

	def __str__(self):
		return f'{self.id},{self.token_id},{self.date},{self.time},{self.terminal_id},{self.transaction_type_id},{self.amount}'
transaction_history_out = []
@dataclasses.dataclass
class Transaction_History(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	transaction_id: int = dataclasses.field(init=False)
	event_id: int = dataclasses.field(init=False)
	timestamp: datetime = dataclasses.field(init=False)
	value: int = dataclasses.field(init=False)
	in_seq_pos: int = dataclasses.field(init=False)

	transactions:dataclasses.InitVar[typing.Any] = None
	events:dataclasses.InitVar[typing.Any] = None
	def __post_init__(self, transactions=None, events=None):
		self.transaction_id = transactions.id
		random_events = events_dict[random.randrange(len(events_dict))]
		self.event_id = random_events["id"]
		delta = datetime.timedelta(seconds = random.randrange(10))
		self.timestamp = datetime.datetime.combine(transactions.date, transactions.time) + delta
		self.value = None
		self.in_seq_pos = random.randrange(1, 5)
		# transaction_history_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.transaction_id},{self.event_id},{self.timestamp},{self.value},{self.in_seq_pos}'
shops_out = []
@dataclasses.dataclass
class Shops(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	street_name: str = dataclasses.field(init=False)
	street_num: int = dataclasses.field(init=False)
	postal_code: str = dataclasses.field(init=False)
	city: str = dataclasses.field(init=False)
	company: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.street_num = self.random_int(1, 50)

		shops_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.street_name},{self.street_num},{self.postal_code},{self.city},{self.company}'
events_out = []
@dataclasses.dataclass
class Events(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	code: str = dataclasses.field(init=False)
	description: str = dataclasses.field(init=False)
	has_timestamp: bool = dataclasses.field(init=False)
	has_value: bool = dataclasses.field(init=False)

	def __post_init__(self):
		self.code = self.random_item(population=['crs', 'cr', 'cp', 'pofs', 'pofc', 'poff', 'pofv', 'ofd', 'ofa', 'pons', 'ponc', 'onr', '2ar', 'ss', 'sf', 'sv'])
		if self.code == 'crs':
			self.description = 'Card read started'
		if self.code == 'cr':
			self.description = 'Card read'
		if self.code == 'cp':
			self.description = 'CDCVM performed'
		if self.code == 'pofs':
			self.description = 'Offline PIN started'
		if self.code == 'pofc':
			self.description = 'Offline PIN canceled'
		if self.code == 'poff':
			self.description = 'Offline PIN failed'
		if self.code == 'pofv':
			self.description = 'Offline PIN entered'
		if self.code == 'ofd':
			self.description = 'Offline declined'
		if self.code == 'ofa':
			self.description = 'Offline approved'
		if self.code == 'pons':
			self.description = 'Online PIN started'
		if self.code == 'ponc':
			self.description = 'Online PIN canceled'
		if self.code == 'onr':
			self.description = 'Online result'
		if self.code == '2ar':
			self.description = '2nd AC rejected'
		if self.code == 'ss':
			self.description = 'Signature started'
		if self.code == 'sf':
			self.description = 'Signature failed'
		if self.code == 'sv':
			self.description = 'Signature verified'

		events_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.code},{self.description},{self.has_timestamp},{self.has_value}'
card_types_out = []
@dataclasses.dataclass
class Card_Types(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	name: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.name = self.random_item(population=['Contact EMV', 'Contactless EMV', 'Contactless Magstripe', 'Magstripe'])

		card_types_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.name}'
transaction_type_out = []
@dataclasses.dataclass
class Transaction_Type(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	values: str = dataclasses.field(init=False)

	def __post_init__(self):
		self.values = self.random_item(population=['Sale Transaction', 'Reverse Authorization', 'Refund Transaction'])

		transaction_type_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.values}'
terminals_out = []
@dataclasses.dataclass
class Terminals(DataUtil.DataUtil):
	id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
	shop_id: int = dataclasses.field(init=False)

	shop:dataclasses.InitVar[typing.Any] = None
	def __post_init__(self, shop=None):
		self.shop_id = shop.id

		terminals_out.append(dataclasses.asdict(self))
	def __str__(self):
		return f'{self.id},{self.shop_id}'

if __name__ == "__main__":
	for i in range(1000):
		print(Token())
	# print(transactions_out)
	# print(transaction_history_out)
    # print(Transactions())
    # print(Transaction_History())
    # print(Shops())
    # print(Events())
    # print(Card_Types())
    # print(Transaction_Type())
    # print(Terminals())

keys = token_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/token.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(token_out)
keys = transactions_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/transactions.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(transactions_out)
keys = transaction_history_out[0].keys()
a_file = open(f"{str(DATASET_PATH)}/output/transaction_history.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(transaction_history_out)
# keys = shops_out[0].keys()
# a_file = open(f"{str(DATASET_PATH)}/output/shops.csv", "w")
# dict_writer = csv.DictWriter(a_file, keys)
# dict_writer.writeheader()
# dict_writer.writerows(shops_out)
# keys = events_out[0].keys()
# a_file = open(f"{str(DATASET_PATH)}/output/events.csv", "w")
# dict_writer = csv.DictWriter(a_file, keys)
# dict_writer.writeheader()
# dict_writer.writerows(events_out)
# keys = card_types_out[0].keys()
# a_file = open(f"{str(DATASET_PATH)}/output/card_types.csv", "w")
# dict_writer = csv.DictWriter(a_file, keys)
# dict_writer.writeheader()
# dict_writer.writerows(card_types_out)
# keys = transaction_type_out[0].keys()
# a_file = open(f"{str(DATASET_PATH)}/output/transaction_type.csv", "w")
# dict_writer = csv.DictWriter(a_file, keys)
# dict_writer.writeheader()
# dict_writer.writerows(transaction_type_out)
# keys = terminals_out[0].keys()
# a_file = open(f"{str(DATASET_PATH)}/output/terminals.csv", "w")
# dict_writer = csv.DictWriter(a_file, keys)
# dict_writer.writeheader()
# dict_writer.writerows(terminals_out)
