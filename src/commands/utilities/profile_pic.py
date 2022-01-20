from discord_slash.utils.manage_commands import create_option

class ClearCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="foto_de_prefil",
            description="Pegue a foto de perfil de um usuário e envie aqui",
            options=[
                create_option(
                    name="usuario",
                    description="O nome do usuário que você deseja pegar a foto de perfil",
                    option_type=3,
                    required=True
                )
            ],
            guild_ids=e.allowed_guilds["default"]
        )
        async def limpar(ctx, quantidade=10):
            return