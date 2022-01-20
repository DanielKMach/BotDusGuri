from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_commands import remove_all_commands
from asyncio import sleep

class AddGameCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="adicionar_jogo",
            description="Lista de Jogos - Adicione um jogo à lista",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo que você deseja adicionar",
                    option_type=3,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds["gamelist"]
        )
        async def adicionar_jogo(ctx, nome_do_jogo):

            #msg = await ctx.send(f":hourglass_flowing_sand: | Carregando...")

            e.gamelist.create_game(
                nome_do_jogo,
                added_by=ctx.author.id
            )
            e.gamelist.sort()
            e.gamelist.save_to_mongo()

            await ctx.send(content=f":white_check_mark: | **{nome_do_jogo}** adicionado com sucesso!")