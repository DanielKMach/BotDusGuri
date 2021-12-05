from discord_slash.utils.manage_commands import create_option

class ReviewGameCommand:

    def __init__(self, e):
        @e.slash.slash(
            name="avaliar_jogo",
            description="Lista de Jogos - Dê uma nota e sua opinião sobre um jogo!",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo que você deseja avaliar",
                    option_type=3,
                    required=True,
                    choices=e.gamelist.get_choices()
                ),
                create_option(
                    name="nota",
                    description="A Nota do jogo de `0` a `10`",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="opinião",
                    description="A sua opinião sobre o jogo",
                    option_type=3,
                    required=False
                )
            ],
            guild_ids=e.allowed_guilds["gamelist"]
        )
        async def avaliar_jogo(ctx, nome_do_jogo, nota, opinião=None):
            try:
                nota = float(nota)
                nota = max(min(nota, 10), 0)
            except:
                await ctx.send(":warning: | Esta nota é inválida")
                return
            
            e.gamelist.rate_game(
                e.gamelist.index_of(nome_do_jogo), ctx.author.id, nota, opinion=opinião
            )
            e.gamelist.save_to_mongo()
            await ctx.send(f":star: | **{ctx.author.display_name}** avaliou o jogo **{nome_do_jogo}** com `{str(nota)}/10`!")
