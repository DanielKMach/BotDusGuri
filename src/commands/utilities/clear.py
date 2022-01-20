from discord_slash.utils.manage_commands import create_option

class ClearCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="limpar",
            description="Limpe em sequência com este comando.",
            options=[
                create_option(
                    name="quantidade",
                    description="A quantidade de mensagens que você deseja excluir em sequência",
                    option_type=3,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds["default"]
        )
        async def limpar(ctx, quantidade=10):
            return