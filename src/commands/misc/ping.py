
class PingCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="ping",
            description="A latência entre eu e você",
            guild_ids=e.allowed_guilds["default"]
        )
        async def ping(ctx):
            await ctx.send(f"<:good_connection:746225743956148294> | O ping atual é de **{str(int(e.bot.latency * 1000))}ms**")
            [][0]