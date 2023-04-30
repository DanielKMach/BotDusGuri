import discord
import bdg

class ViewGameCommand(bdg.BdgCommand):

	header = {
		'name': "ver_jogo",
		'description': "Lista de Jogos - Veja os detalhes de um jogo com este comando"
	}

	async def on_command(self, i: discord.Interaction, nome_do_jogo: str):

		gamelist = self.bdg.get_gamelist(self.bdg.guild_collection(i.guild))
		game = gamelist[nome_do_jogo]

		if not game:
			await i.response.send_message(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return

		game_embed = discord.Embed(
			title=game.name,
			color=0x00b934
		)

		# Definir icone no Embed
		if game.icon:
			game_embed.set_thumbnail(url=game.icon)

		# Definir fonte no Embed
		if game.source:
			game_embed.url = game.source

		# Define quem adicionou o jogo no Embed
		if game.added_by:
			added_by = await self.bdg.fetch_user(game.added_by)
			game_embed.set_footer(
				icon_url=added_by.display_avatar,
				text="Jogo adicionado por " + added_by.display_name
			)

		# Carrega as avaliações para o Embed
		reviews = game.reviews
		if len(reviews) > 0:
			ratings_text = ""
			for review in reviews:
				rating_author = await self.bdg.fetch_user(int(review.author))
				ratings_text += f"{rating_author.mention} - `{review.rating}/10`"
				if review.opinion:
					ratings_text += f" *\"{review.opinion}\"*"
				
				ratings_text += "\n"

			game_embed.add_field(
				name=f":star: | Avaliações ({game.rating_median}/10)",
				value=ratings_text,
				inline=False
			)

		await i.response.send_message(f":bookmark_tabs: | Aqui estão algumas informações sobre **{game.name}**", embed=game_embed)