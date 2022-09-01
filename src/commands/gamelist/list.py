from discord import Interaction, Embed, app_commands
from bdg import BotDusGuri

class ListGamesCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "lista_de_jogos",
			description= "Lista de Jogos - Visualize a lista de jogos disponiveis para jogar",
			callback= self.on_command
		)

	
	async def on_command(self, i: Interaction):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))

		game_names = gamelist.get_name_list()
		game_ratings = gamelist.get_rating_median_list()

		if len(game_names) == 0:
			await i.response.send_message(":cricket: | Não há jogos na lista", ephemeral=True)
			return

		# Contruindo a lista
		message = str()
		for g in range(len(game_names)):
			message += f"{game_names[g]} - "
			if game_ratings[g] != None:
				message += f"`{game_ratings[g]}/10`"
			else:
				message += "`Sem avaliações`"

			if gamelist.has_user_rated_game(g, i.user.id):
				message += " :star:"
			message += "\n"

		ratings_count = 0
		for rating in game_ratings:
			if rating != None:
				ratings_count += 1

		# Montando o Embed
		list_embed = Embed(
			title="Lista de Jogos",
			description=message,
			color=0x0090eb
		)
		list_embed.set_footer(
			text=f"{ratings_count}/{len(game_names)} avaliados"
		)

		await i.response.send_message(":scroll: | Aqui está a lista de jogos disponiveis para jogar", embed=list_embed)