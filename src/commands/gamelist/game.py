from discord import Interaction, Embed, app_commands
from bdg import BotDusGuri

class ViewGameCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "ver_jogo",
			description= "Lista de Jogos - Veja os detalhes de um jogo com este comando",
			callback= self.on_command
		)

	async def on_command(self, i: Interaction, nome_do_jogo: str):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))

		game_index = gamelist.index_of_closest(nome_do_jogo)
		if game_index == None:
			await i.response.send_message(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return

		name = gamelist.get_name(game_index)
		game_embed = Embed(
			title=name,
			color=0x00b934
		)

		# Definir icone no Embed
		icon_url = gamelist.get_icon(game_index)
		if type(icon_url) == str:
			game_embed.set_thumbnail(url=icon_url)

		# Definir fonte no Embed
		source = gamelist.get_source(game_index)
		if type(source) == str:
			game_embed.url = source

		# Define quem adicionou o jogo no Embed
		added_by_id = gamelist.get_added_by(game_index)
		if added_by_id != None:
			added_by = await self.bot.fetch_user(added_by_id)
			game_embed.set_footer(
				icon_url=added_by.display_avatar,
				text="Jogo adicionado por " + added_by.display_name
			)

		# Carrega as avaliações para o Embed
		ratings = gamelist.get_ratings(game_index)
		if len(ratings) != 0:
			ratings_text = ""
			for rating in ratings:
				rating_author = await self.bot.fetch_user(rating['author'])
				ratings_text += f"{rating_author.mention} - `{rating['rating']}/10`"
				if rating.get('opinion', None) != None:
					ratings_text += f" *\"{rating['opinion']}\"*"
				ratings_text += "\n"

			game_embed.add_field(
				name=f":star: | Avaliações ({gamelist.get_rating_median(game_index)}/10)",
				value=ratings_text,
				inline=False
			)

		await i.response.send_message(f":bookmark_tabs: | Aqui estão algumas informações sobre **{name}**", embed=game_embed)