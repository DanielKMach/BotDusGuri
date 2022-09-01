import bdg
import discord
from commands.utilities import pogoraids

class PogoResearchCommand(discord.app_commands.Command):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "pogo_pesquisas",
			description= "Um gráfico mostrando as atuais recompensas das pesquisas no Pokémon GO",
			callback= self.on_command
		)

	async def on_command(self, i: discord.Interaction):

		await i.response.defer(thinking=True)

		graphic = pogoraids.get_graphic("https://www.leekduck.com/research/")

		await i.followup.send(":scroll: | Aqui estão as atuais recompensas de pesquisa")
		await i.channel.send(graphic)