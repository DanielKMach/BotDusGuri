import io
import bdg
import bs4
import discord
import requests

def download_graphic(leekduck: str) -> discord.File | None:
	try:
		with requests.get(leekduck, cookies={"lang": "pt"}) as web:
			html = bs4.BeautifulSoup(web.content, "html.parser")

		# Pega a url do elemento do DOM e formata para ser usável
		url: str = "https://www.leekduck.com" + html.select_one("#graphic img")['src']
		url = url.replace('..', '')
		url = url.replace(' ', '%20')
		
		# Baixa o gráfico apartir da url
		with requests.get(url) as graphic:
			return discord.File(io.BytesIO(graphic.content), "grafico.png")
	
	except:
		return None

class PokegoCommand(discord.app_commands.Group, name="pokego", description="Últimas notícias do Pokemon GO"):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__()

	@discord.app_commands.command(name="raids", description="Um gráfico mostrando os atuais pokémon em raids no Pokémon GO")
	async def raids(self, i: discord.Interaction):
		await i.response.defer(thinking=True)

		graphic = download_graphic("https://www.leekduck.com/boss/")
		if graphic == None:
			await i.followup.send(":warning: | Não foi possível adiquirir o gráfico. Por favor, tente novamente mais tarde", ephemeral=True)
			return

		await i.followup.send(":rhino: | Aqui estão os atuais pokémon em raids:", file=graphic)


	@discord.app_commands.command(name="pesquisas", description="Um gráfico mostrando as atuais recompensas de pesquisa no Pokémon GO")
	async def research(self, i: discord.Interaction):
		await i.response.defer(thinking=True)

		graphic = download_graphic("https://www.leekduck.com/research/")
		if graphic == None:
			await i.followup.send(":warning: | Não foi possível adiquirir o gráfico. Por favor, tente novamente mais tarde", ephemeral=True)
			return

		await i.followup.send(":scroll: | Aqui estão as atuais recompensas de pesquisa:", file=graphic)

	