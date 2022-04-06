from discord import Client
import os

from dispatch import Dispatcher

TOKEN = os.getenv('TEST_BOT_TOKEN')

class CustomClient(Client):
	async def on_ready(self):
		print(f'{self.user.name} now connected. 🎃')

	async def on_message(self, message):
		if message.author == self.user:
			return
		
		await dispatcher.dispatch(message)
		
	async def on_raw_reaction_add(self, payload):
		guild = self.get_guild(payload.guild_id)
		user = guild.get_member(payload.user_id)
		if user == self.user:
			return

		channel = self.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)

client = CustomClient()
dispatcher = Dispatcher(client)

client.run(TOKEN)
