
class PingCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="ping",
            description="A latência entre eu e você"
        )
        async def ping(ctx):
            await ctx.send(f"<:good_connection:746225743956148294> | O ping atual é de **{str(int(e.bot.latency * 1000))} milissegundos**")