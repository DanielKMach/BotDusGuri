from discord import Interaction, Embed, app_commands
import bdg

class ListGamesCommand(bdg.BdgCommand):

	header = {
		'name': "lista_de_jogos",
		'description': "Lista de Jogos - Visualize a lista de jogos disponiveis para jogar",
	}
	
	async def on_command(self, i: Interaction):

		gamelist = self.bdg.get_gamelist(self.bdg.guild_collection(i.guild))

		names = [ game.name for game in gamelist.games ]
		medians = [ game.rating_median for game in gamelist.games ]
		rated = [ game.index_of_user_rating(i.user.id) != None for game in gamelist.games ]

		if len(names) == 0:
			await i.response.send_message(":cricket: | Não há jogos na lista", ephemeral=True)
			return

		# Contruindo a descrição do Embed
		message = str()
		for g in range(len(names)):
			message += f"{names[g]} - "

			if medians[g]:
				message += f"`{medians[g]}/10`"
			else:
				message += "`Sem avaliações`"

			if rated[g]:
				message += " :star:"
			message += "\n"

		rated_games_count = len(medians) - medians.count(None)

		# Montando o Embed
		list_embed = Embed(
			title="Lista de Jogos",
			description=message,
			color=0x0090eb
		)
		list_embed.set_footer(
			text=f"{rated_games_count}/{len(names)} avaliados"
		)

		await i.response.send_message(":scroll: | Aqui está a lista de jogos disponiveis para jogar", embed=list_embed)