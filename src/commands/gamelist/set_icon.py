from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

def define_seticon_command(e):

	@e.slash.slash(
		name="definir_icone",
		description="Lista de Jogos - Define um link como o ícone de um jogo",
		options=[
			create_option(
				name="nome_do_jogo",
				description="O nome do jogo para definir o ícone",
				option_type=SlashCommandOptionType.STRING,
				required=True
			),
			create_option(
				name="link",
				description="O link da imagem para definir como ícone",
				option_type=SlashCommandOptionType.STRING,
				required=True
			)
		],
		guild_ids=e.allowed_guilds["gamelist"]
	)
	async def definir_icone(ctx, nome_do_jogo, link):
		game_index = e.gamelist.index_of_closest(nome_do_jogo)
		if game_index == None:
			await ctx.send(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**")
			return

		e.gamelist.set_icon(game_index, link.lower())

		await ctx.send(f":link: | Definido ícone de **{e.gamelist.get_name(game_index)}**")
		e.gamelist.save_to_mongo()

