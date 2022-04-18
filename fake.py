@dataclasses.dataclass
class Comments(DataUtil):
	url: str = field(default_factory=itertools.count(start=1).__next__)
	source_system: str = field(init=False)
	created_at: datetime = field(init=False)
	comment_text: str = field(init=False)
	comment_reference: str = field(init=False)
	user_name: str = field(init=False)

	def __post_init__(self):
		self.source_system = self.random_item(population=['GMB', 'YT'])
		self.created_at = self.created_at(datetime.datetime(2022, 1, 1))
		self.comment_text = ##FILL ME IN
		self.comment_reference = ##FILL ME IN
		self.user_name = ##FILL ME IN

		def __str__(self):
			return f'{self.url},{self.source_system},{self.created_at},{self.comment_text},{self.comment_reference},{self.user_name}'

@dataclasses.dataclass
class Products(DataUtil):
	id: int = field(default_factory=itertools.count(start=1).__next__)
	offer_id: int = field(init=False)
	title: str = field(init=False)
	description: str = field(init=False)
	link: str = field(init=False)
	image_link: str = field(init=False)
	channel: str = field(init=False)
	availability: str = field(init=False)
	price: float = field(init=False)
	gtin: str = field(init=False)
	google_product_category_path: str = field(init=False)

	def __post_init__(self):
		self.offer_id = ##FILL ME IN
		self.title = ##FILL ME IN
		self.description = ##FILL ME IN
		self.link = ##FILL ME IN
		self.image_link = ##FILL ME IN
		self.channel = ##FILL ME IN
		self.availability = ##FILL ME IN
		self.price == self.random_int(0, 100)
		self.gtin = ##FILL ME IN
		self.google_product_category_path = ##FILL ME IN

		def __str__(self):
			return f'{self.id},{self.offer_id},{self.title},{self.description},{self.link},{self.image_link},{self.channel},{self.availability},{self.price},{self.gtin},{self.google_product_category_path}'

@dataclasses.dataclass
class Inventory(DataUtil):
	product_id: str = field(init=False)
	store_code: str = field(init=False)
	availability: str = field(init=False)
	quantity: int = field(init=False)

	products:InitVar[Any] = None
	def __post_init__(self, products=None):
		self.product_id == products.id
		self.store_code = ##FILL ME IN
		self.availability = ##FILL ME IN
		self.quantity == self.random_int(0, 5)

		def __str__(self):
			return f'{self.product_id},{self.store_code},{self.availability},{self.quantity}'

@dataclasses.dataclass
class Stores(DataUtil):
	store_code: str = field(init=False)
	location: coordinate = field(init=False)
	store_name: str = field(init=False)

	def __post_init__(self):
		self.store_code = ##FILL ME IN
		self.location = ##FILL ME IN
		self.store_name = self.random_item(population=['store1', 'store2'])

		def __str__(self):
			return f'{self.store_code},{self.location},{self.store_name}'

@dataclasses.dataclass
class Customers(DataUtil):
	id: int = field(default_factory=itertools.count(start=1).__next__)
	gender: str = field(init=False)
	first_name: str = field(init=False)
	last_name: str = field(init=False)
	loyalty_id: str = field(init=False)

	def __post_init__(self):
		self.gender = self.random_item(population=['male', 'female', 'nonbinary'])
		if self.gender == 'male':
			self.first_name = fake.first_name_male()
		if self.gender == 'female':
			self.first_name = fake.first_name_female()
		if self.gender == 'nonbinary':
			self.first_name = fake.first_name_nonbinary()
		self.last_name = fake.last_name_nonbinary()
		self.loyalty_id = ##FILL ME IN

		def __str__(self):
			return f'{self.id},{self.gender},{self.first_name},{self.last_name},{self.loyalty_id}'

@dataclasses.dataclass
class Transactions(DataUtil):
	id: int = field(default_factory=itertools.count(start=1).__next__)
	customer_id: int = field(init=False)
	product_id: int = field(init=False)
	cost: float = field(init=False)

	customers:InitVar[Any] = None
	products:InitVar[Any] = None
	def __post_init__(self, customers=None, products=None):
		self.customer_id == customers.id
		self.product_id == products.id
		self.cost == self.random_int(0, 100)

		def __str__(self):
			return f'{self.id},{self.customer_id},{self.product_id},{self.cost}'

