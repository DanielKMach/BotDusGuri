import discord
import bdg

__all__ = [ "PingCommand" ]

class PingCommand(discord.app_commands.Command):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__(
			name="ping",
			description="A lantência entre eu e você!",
			callback=self.on_command
		)

	async def on_command(self, i: discord.Interaction):
		await i.response.send_message(f":ping_pong: | O ping atual é de **{int(self.bot.latency * 1000)}ms**", ephemeral=True)