
class TestCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="teste",
            description="Comando teste",
            guild_ids=e.allowed_guilds
        )
        async def teste(ctx):
            await ctx.send(f"<:diamond:746850016865288202> | Testado com sucesso")