from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

def define_setname_command(e):

	@e.slash.slash(
		name="renomear_jogo",
		description="Lista de Jogos - Renomeie algum jogo que você nomeou errado",
		options=[
			create_option(
				name="nome_do_jogo",
				description="O nome atual do jogo para ser renomeado",
				option_type=SlashCommandOptionType.STRING,
				required=True
			),
			create_option(
				name="novo_nome",
				description="O novo nome do jogo",
				option_type=SlashCommandOptionType.STRING,
				required=True
			)
		],
		guild_ids=e.allowed_guilds["gamelist"]
	)
	async def renomear_jogo(ctx, nome_do_jogo, novo_nome):
		game_index = e.gamelist.index_of_closest(nome_do_jogo)
		if game_index == None:
			await ctx.send(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**")
			return

		old_name = e.gamelist.get_name(game_index)
		e.gamelist.set_name(game_index, novo_nome)
		e.gamelist.save_to_mongo()
		new_name = e.gamelist.get_name(game_index)

		await ctx.send(f":pencil: | **{old_name}** agora se chama **{new_name}**!")
