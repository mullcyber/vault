from abc import ABC, abstractmethod

class Command(ABC):
	name = None

	roles = []
	channels = []
	categories = []
	delete_msg = False

	def __init__(self, client, msg, dispatcher):
		self.client = client
		self.msg = msg
		self.dispatcher = dispatcher

	@classmethod
	@abstractmethod
	def register_parameters(cls, prefix, subparsers):
		...

	@classmethod
	def create_parser(cls, prefix, subparsers):
		parser = subparsers.add_parser(f"{prefix}{cls.name}")
		parser.set_defaults(cls=cls)
		return parser
		
	@abstractmethod
	def execute(self):
		...
