from discord_slash.utils.manage_commands import create_option
from math import *

class CalculateCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="calculo",
            description="Uma calculadora em forma de chat!",
            options=[
                create_option(
                    name="expressão",
                    description="Uma expressão matemática",
                    option_type=3,
                    required=True
                ),
            ]
        )
        async def calculo(ctx, expressão):
            try:
                solution = eval(expressão)
            except:
                await ctx.send(":warning: | Desculpa mas eu não consigo calcular isto")
                return

            await ctx.send(f":abacus: | `{expressão}` = **{str(solution)}**")