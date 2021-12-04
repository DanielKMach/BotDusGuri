from discord_slash.utils.manage_commands import create_option
from discord import Embed

class GameCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="ver_jogo",
            description="Lista de Jogos - Veja mais detalhes sobre um jogo especifico",
            options=[
                create_option(
                    name="nome_do_jogo",
                    description="O nome do jogo para ver mais sobre ele",
                    option_type=3,
                    required=True,
                    choices=e.gamelist.get_choices()
                )
            ],
            guild_ids=e.allowed_guilds
        )
        async def ver_jogo(ctx, nome_do_jogo):
            game_index = e.gamelist.index_of(nome_do_jogo)

            game_embed = Embed(
                title=e.gamelist.get_name(game_index),
                color=0x00b934
            )

            icon_url = e.gamelist.get_icon(game_index)
            if type(icon_url) == str:
                game_embed.set_thumbnail(url=icon_url)
                #game_embed.set_thumbnail(url=ctx.author.avatar_url)
                print(icon_url)
                print(ctx.author.avatar_url)

            source = e.gamelist.get_source(game_index)
            if type(source) == str:
                game_embed.url = source

            added_by = e.gamelist.get_added_by(game_index)
            if added_by != None:
                added_by_user = await e.bot.fetch_user(added_by)
                game_embed.set_footer(
                    icon_url=added_by_user.avatar_url,
                    text="Jogo adicionado por " + added_by_user.display_name
                )

            ratings = e.gamelist.get_ratings(game_index)
            if len(ratings) != 0:
                ratings_text = ""
                for rating in ratings:
                    rating_author = await e.bot.fetch_user(rating['author'])
                    ratings_text += f"{rating_author.mention} - `{rating['rating']}/10`"
                    if rating.get("opinion", None) != None:
                        ratings_text += f" *\"{rating['opinion']}\"*"
                    ratings_text += "\n"

                game_embed.add_field(
                    name=f":star: | Avaliações ({e.gamelist.get_rating_median(game_index)}/10)",
                    value=ratings_text,
                    inline=False
                )

            await ctx.send(f":bookmark_tabs: | Aqui estão algumas informações sobre **{e.gamelist.get_name(game_index)}**", embed=game_embed)
