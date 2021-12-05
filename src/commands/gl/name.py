from discord_slash.utils.manage_commands import create_option

class SetNameCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="definir_nome",
            description="Lista de Jogos - Renomeie algum jogo que você nomeou errado",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome atual do jogo para ser renomeado",
                    option_type=3,
                    required=True,
                    choices=e.gamelist.get_choices()
                ),
                create_option(
                    name="novo_nome",
                    description="O novo nome do jogo",
                    option_type=3,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds["gamelist"]
        )
        async def definir_nome(ctx, nome_do_jogo, novo_nome):
            game_index = e.gamelist.index_of(nome_do_jogo)

            old_name = e.gamelist.get_name(game_index)
            e.gamelist.set_name(game_index, novo_nome)

            await ctx.send(f":pencil: | **{old_name}** agora se chama **{e.gamelist.get_name(game_index)}**!")
            e.gamelist.writer.save_gamelist()

            await e.slash.sync_all_commands()
