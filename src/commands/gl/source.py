from discord_slash.utils.manage_commands import create_option

class SetSourceCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="definir_fonte",
            description="Lista de Jogos - Define um link como a fonte de um jogo",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo para definir a fonte",
                    option_type=3,
                    required=True,
                    choices=e.gamelist.get_choices()
                ),
                create_option(
                    name="fonte",
                    description="Um link da internet, provavelmente levando ao Google Play",
                    option_type=3,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds["gamelist"]
        )
        async def definir_fonte(ctx, nome_do_jogo, fonte):
            e.gamelist.set_source(e.gamelist.index_of(nome_do_jogo), fonte.lower())
            
            await ctx.send(f":link: | Definido `{fonte.lower()}` como a fonte de **{e.gamelist.get_name(e.gamelist.index_of(nome_do_jogo))}**")
            save_gamelist()
