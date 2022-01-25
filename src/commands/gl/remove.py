from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

class RemoveGameCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="remover_jogo",
            description="Lista de Jogos - Remova um jogo à lista",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo que você deseja remover",
                    option_type=SlashCommandOptionType.STRING,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds["gamelist"]
        )
        async def remover_jogo(ctx, nome_do_jogo):
            game_index = e.gamelist.index_of_closest(nome_do_jogo)
            if game_index == None:
                await ctx.send(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**")
                return

            name = e.gamelist.get_name(game_index)
            e.gamelist.remove_game(game_index)
            e.gamelist.save_to_mongo()
            
            await ctx.send(f":white_check_mark: | **{name}** removido!")