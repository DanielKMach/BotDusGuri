from discord_slash.utils.manage_commands import create_option

class RemoveGameCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="remover_jogo",
            description="Lista de Jogos - Remova um jogo à lista",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo que você deseja remover",
                    option_type=3,
                    required=True,
                    choices=e.gamelist.get_choices()
                )
            ],
            guild_ids=e.allowed_guilds
        )
        @e.slash.permission(
            guild_id=e.allowed_guilds[0],
            permissions=e.default_permissions
        )
        async def remover_jogo(ctx, nome_do_jogo):
            e.gamelist.remove_game(
                e.gamelist.index_of(nome_do_jogo)
            )
            e.gamelist.save_to_mongo()
            await ctx.send(f":white_check_mark: | **{nome_do_jogo}** removido!")
            await e.slash.sync_all_commands()