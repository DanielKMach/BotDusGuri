from discord_slash.utils.manage_commands import create_option
from random import randint
from discord_slash.model import SlashCommandOptionType

class RollCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="roleta",
            description="Um número aleatório!",
            options=[
                create_option(
                    name="mínimo",
                    description="Valor mínimo para sortear",
                    option_type=SlashCommandOptionType.INTEGER,
                    required=False
                ),
                create_option(
                    name="máximo",
                    description="Valor máximo para sortear",
                    option_type=SlashCommandOptionType.INTEGER,
                    required=False
                ),
            ],
            guild_ids=e.allowed_guilds["default"]
        )
        async def roleta(ctx, mínimo=1, máximo=10):
            await ctx.send(f":game_die: | A roleta entre `{mínimo}` e `{máximo}` deu... **{randint(mínimo, máximo)}**!")