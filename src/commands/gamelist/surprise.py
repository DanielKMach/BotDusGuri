from discord import app_commands
import discord
import bdg
import gamelist
import random

class SurpriseGameCommand(app_commands.Command):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__(
			name="sortear_jogo",
			description="Lista de Jogos - Sorteie um jogo aleatório baseado no filtro especificado",
			callback=self.on_command
		)

	async def on_command(self, i: discord.Interaction, filtro: gamelist.GameFilter):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))

		available_games = [ g for g in gamelist.filter(filtro) ]

		if len(available_games) <= 0:
			await i.response.send_message(":warning: | Não há nenhum jogo disponível com esse filtro", ephemeral=True)
			return

		game_index = available_games[ random.randint(0, len(available_games) - 1) ]
		game = gamelist[game_index]
		await i.response.send_message(f":tada: | O jogo sorteado é... ||**{game.name.upper()}!**||")

