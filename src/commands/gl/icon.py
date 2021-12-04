from discord_slash.utils.manage_commands import create_option

class SetIconCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="definir_icone",
            description="Lista de Jogos - Define um link como o ícone de um jogo",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo para definir o ícone",
                    option_type=3,
                    required=True,
                    choices=e.gamelist.get_choices()
                ),
                create_option(
                    name="link",
                    description="Um link da internet, provavelmente levando ao Google Play",
                    option_type=3,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds
        )
        @e.slash.permission(
            guild_id=e.allowed_guilds[0],
            permissions=e.default_permissions
        )
        async def definir_icone(ctx, nome_do_jogo, link):
            e.gamelist.set_icon(e.gamelist.index_of(nome_do_jogo), link.lower())

            await ctx.send(f":link: | Definido ícone de **{e.gamelist.get_name(e.gamelist.index_of(nome_do_jogo))}**")
            e.gamelist.save_to_mongo()

