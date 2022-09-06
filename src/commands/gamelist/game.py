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
		game = gamelist[nome_do_jogo]

		if not game:
			await i.response.send_message(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return

		game_embed = Embed(
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
			added_by = await self.bot.fetch_user(game.added_by)
			game_embed.set_footer(
				icon_url=added_by.display_avatar,
				text="Jogo adicionado por " + added_by.display_name
			)

		# Carrega as avaliações para o Embed
		ratings = game.ratings
		if len(ratings) > 0:
			ratings_text = ""
			for rating in ratings:
				rating_author = await self.bot.fetch_user(rating['author'])
				ratings_text += f"{rating_author.mention} - `{rating['rating']}/10`"
				if rating.get('opinion', None) != None:
					ratings_text += f" *\"{rating['opinion']}\"*"
				ratings_text += "\n"

			game_embed.add_field(
				name=f":star: | Avaliações ({game.rating_median}/10)",
				value=ratings_text,
				inline=False
			)

		await i.response.send_message(f":bookmark_tabs: | Aqui estão algumas informações sobre **{game.name}**", embed=game_embed)