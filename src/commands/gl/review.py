from discord_slash.utils.manage_commands import create_option
from utils import OptionTypes

class ReviewGameCommand:

    def __init__(self, e):
        @e.slash.slash(
            name="avaliar_jogo",
            description="Lista de Jogos - Dê uma nota e sua opinião sobre um jogo!",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo que você deseja avaliar",
                    option_type=OptionTypes.STRING,
                    required=True
                ),
                create_option(
                    name="nota",
                    description="A Nota do jogo de `0` a `10`",
                    option_type=OptionTypes.NUMBER,
                    required=True
                ),
                create_option(
                    name="opinião",
                    description="A sua opinião sobre o jogo",
                    option_type=OptionTypes.STRING,
                    required=False
                )
            ],
            guild_ids=e.allowed_guilds["gamelist"]
        )
        async def avaliar_jogo(ctx, nome_do_jogo, nota, opinião=None):
            game_index = e.gamelist.index_of_closest(nome_do_jogo)
            if game_index == None:
                await ctx.send(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**")
                return
            
            try:
                nota = float(nota)
                nota = max(min(nota, 10), 0)
            except:
                await ctx.send(":warning: | Esta nota é inválida")
                return
            
            e.gamelist.rate_game(game_index, ctx.author.id, nota, opinion=opinião)
            e.gamelist.save_to_mongo()

            await ctx.send(f":star: | **{ctx.author.display_name}** avaliou o jogo **{e.gamelist.get_name(game_index)}** com `{str(nota)}/10`!")
