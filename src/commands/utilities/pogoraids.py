import bdg
import bs4
import discord
import requests

class PogoRaidsCommand(discord.app_commands.Command):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "pogo_raids",
			description= "Um gráfico mostrando os atuais pokémon em raids no Pokémon GO",
			callback= self.on_command
		)

	async def on_command(self, i: discord.Interaction):

		await i.response.defer(thinking=True)

		html = bs4.BeautifulSoup(requests.get("https://www.leekduck.com/boss", cookies={"lang": "pt"}).content, "html.parser")

		graphic = html.select_one("#graphic img")['src']

		await i.followup.send(content=graphic)