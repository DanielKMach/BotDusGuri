import bdg
import bs4
import discord
import requests

def get_graphic(url: str) -> str:

	html = bs4.BeautifulSoup(requests.get(url, cookies={"lang": "pt"}).content, "html.parser")
	graphic = "https://www.leekduck.com" + html.select_one("#graphic img")['src']
	graphic = graphic.replace("..", "")
	graphic = graphic.replace(" ", "%20")
	
	return graphic

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

		graphic = get_graphic("https://www.leekduck.com/boss/")

		await i.followup.send(":rhino: | Aqui estão os atuais pokémon em raids")
		await i.channel.send(graphic)