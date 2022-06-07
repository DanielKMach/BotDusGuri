from discord import Embed

def define_viewlist_command(e):

    @e.slash.slash(
        name="lista_de_jogos",
        description="Lista de Jogos - Visualize a lista de jogos disponiveis para jogar",
        guild_ids=e.allowed_guilds["gamelist"]
    )
    async def lista_de_jogos(ctx):

        game_names = e.gamelist.get_name_list()
        game_ratings = e.gamelist.get_rating_median_list()

        if len(game_names) == 0:
            await ctx.send("Não existe jogos na lista")
            return

        # Contruindo a lista
        message = ""
        for i in range(len(game_names)):
            message += f"{game_names[i]} - "
            if game_ratings[i] != None:
                message += f"`{game_ratings[i]}/10`"
            else:
                message += "`Sem avaliações`"

            if e.gamelist.has_user_rated_game(i, ctx.author.id):
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

        await ctx.send(":scroll: | Aqui está a lista de jogos disponiveis para jogar", embed=list_embed)