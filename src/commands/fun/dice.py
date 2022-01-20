from random import randint
from discord import File

class DiceCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="dado",
            description="Um dado de 6 lados",
            guild_ids=e.allowed_guilds["default"]
        )
        async def dado(ctx):
            num = randint(1, 6)
            dice_path = f"res/dices/dice_{num}.gif"

            await ctx.send(file=File(dice_path))