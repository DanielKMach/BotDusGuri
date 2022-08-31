from discord import Interaction, app_commands
from bdg import BotDusGuri
from gamelist import GameFilter
from random import randint

class SurpriseGameCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name="sortear_jogo",
			description="Lista de Jogos - Sorteie um jogo aleatório baseado no filtro especificado",
			callback=self.on_command
		)

	async def on_command(self, i: Interaction, de: GameFilter):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))

		available_games: tuple[int] = (g for g in gamelist.filter(de))

		if len(available_games) <= 0:
			await i.response.send_message(":warning: | Não há nenhum jogo com esse filtro", ephemeral=True)
			return

		game_index = available_games[ randint(0, len(available_games) - 1) ]
		game = gamelist.get_name(game_index)
		await i.response.send_message(f":tada: | O jogo sorteado é... ||**{game.upper()}!**||")

