from discord import Interaction, app_commands
from bdg import BotDusGuri

class ReviewGameCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name="avaliar_jogo",
			description="Lista de Jogos - Dê uma nota e sua opinião sobre um jogo!",
			callback=self.on_command
		)
	
	async def on_command(self, i: Interaction, nome_do_jogo: str, nota: app_commands.Range[float, 0, 10], opinião: str = None):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))

		game = gamelist[nome_do_jogo]
		if not game:
			await i.response.send_message(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return
		
		game.rate(
			author= i.user.id,
			rating= nota,
			opinion= opinião
		)
		gamelist.save_to_mongo()

		await i.response.send_message(f":star: | Você avaliou **{game.name}** com **{nota}/10**!", ephemeral=True)
