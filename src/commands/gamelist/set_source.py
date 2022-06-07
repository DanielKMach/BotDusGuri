from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

def define_setsource_command(e):

	@e.slash.slash(
		name="definir_fonte",
		description="Lista de Jogos - Define um link como a fonte de um jogo",
		options=[
			create_option(
				name="nome_do_jogo",
				description="O nome do jogo para definir a fonte",
				option_type=SlashCommandOptionType.STRING,
				required=True
			),
			create_option(
				name="fonte",
				description="Um link da internet, provavelmente levando ao Google Play",
				option_type=SlashCommandOptionType.STRING,
				required=True
			)
		],
		guild_ids=e.allowed_guilds["gamelist"]
	)
	async def definir_fonte(ctx, nome_do_jogo, fonte):
		game_index = e.gamelist.index_of_closest(nome_do_jogo)
		if game_index == None:
			await ctx.send(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**")
			return
		
		e.gamelist.set_source(game_index, fonte.lower())
		e.gamelist.save_to_mongo()
		
		await ctx.send(f":link: | Definido `{fonte.lower()}` como a fonte de **{e.gamelist.get_name(game_index)}**")
