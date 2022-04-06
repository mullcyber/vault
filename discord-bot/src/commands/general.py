from random import choice

from command import Command
from server import ROLE_TESTROLE, CHANNEL_1, CATEGORY_TEST

def max20(val):
	num = int(val)
	if 0 < num <= 20:
		return num
	raise ValueError("Bad Range")

class DeleteMsg(Command):
	name = "deletemsg"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)
		parser.add_argument('count', type=max20, help="Number of messages to delete")

	async def execute(self, args):
		async for message in self.msg.channel.history(limit=args.count+1):
			await message.delete()
		

class ChooseOption(Command):
	name = "choose"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)
		parser.add_argument('options', nargs='+', type=str, help="Space-separated options to randomly choose from")

	async def execute(self, args):
		option = choice(args.options)
		await self.msg.channel.send(f"Randomly selected: {option}")

class ShowHelp(Command):
	name = "help"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)

	async def execute(self, args):
		text = self.dispatcher.parser.format_help()
		await self.msg.channel.send(text)

class ShowUsage(Command):
	name = "usage"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)

	async def execute(self, args):
		text = self.dispatcher.parser.format_usage()
		await self.msg.channel.send(text)
