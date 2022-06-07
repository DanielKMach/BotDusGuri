from random import randint

def define_sortgames_command(e):

	@e.slash.slash(
		name="sortear_jogo",
		description="Lista de Jogos - Sorteie um jogo aleatório que ainda não foi avaliado",
		guild_ids=e.allowed_guilds["gamelist"]
	)
	async def sortear_jogo(ctx):
		games = e.gamelist.get_name_list()
		games_to_sort = []
		for game in games:
			if not e.gamelist.has_been_rated(e.gamelist.index_of(game)):
				games_to_sort.append(game)

		if len(games_to_sort) == 0:
			await ctx.send(":warning: | Todos os jogos da lista já foram avaliados")
			return

		random_game = games_to_sort[randint(0, len(games_to_sort) - 1)]
		await ctx.send(f":tada: | O jogo sorteado é... ||**{random_game.upper()}!**||")

