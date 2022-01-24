from discord_slash.utils.manage_commands import create_option, create_choice
from discord import Embed
from requests import request
from bs4 import BeautifulSoup

class MetaCommand:

    names = {
        "brawlBall": "FUTE-BRAWL",
        "soloShowdown": "COMBATE SOLO",
        "duoShowdown": "COMBATE DUPLO",
        "gemGrab": "PIQUE-GEMA",
        "bounty": "CAÇA ESTRELAS",
        "hotZone": "ZONA ESTRATÉGICA",
        "knockout": "NOCAUTE",
        "heist": "ROUBO",
        "siege": "ENCURRALADO"
    }

    colors = {
        "brawlBall": 0x8CA0DF,
        "soloShowdown": 0x81D621,
        "duoShowdown": 0x81D621,
        "gemGrab": 0x9B3DF3,
        "bounty": 0x01CFFF,
        "hotZone": 0xE33C50,
        "knockout": 0xF7831C,
        "heist": 0x9B3DF3,
        "siege": 0xF7831C
    }

    def __init__(self, e):

        @e.slash.slash(
            name="metas",
            description="Mostra uma lista dos brawlers metas de cada mapa.",
            options=[
                create_option(
                    name="modo",
                    description="O modo, ex: Futebrawl, Pique-gema, Combate.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="FUTE-BRAWL",
                            value="brawlBall"
                        ),
                        create_choice(
                            name="COMBATE SOLO",
                            value="soloShowdown"
                        ),
                        create_choice(
                            name="COMBATE DUPLO",
                            value="duoShowdown"
                        ),
                        create_choice(
                            name="PIQUE-GEMA",
                            value="gemGrab"
                        ),
                        create_choice(
                            name="CAÇA-ESTRELAS",
                            value="bounty"
                        ),
                        create_choice(
                            name="ZONA ESTRATÉGICA",
                            value="hotZone"
                        ),
                        create_choice(
                            name="NOCAUTE",
                            value="knockout"
                        ),
                        create_choice(
                            name="ROUBO",
                            value="heist"
                        ),
                        create_choice(
                            name="ENCURRALADO",
                            value="siege"
                        )
                    ]
                ),
                create_option(
                    name="top",
                    description="Top 5? Top 10? Top 15?",
                    option_type=4,
                    required=False
                )
            ],
            guild_ids=e.allowed_guilds["default"]
        )
        async def metas(ctx, modo, top=10):
            msg = await ctx.send("Processando...")

            response = request("GET", "https://brawlace.com/meta")

            soup = BeautifulSoup(response.content, "html.parser")

            div = soup.select_one(f"#gameModeData{modo}")
            table = div.select_one(f"table tbody")
            brawlers = table.find_all("tr")

            text = str()

            for i in range(min(len(brawlers), top)):
                info = brawlers[i].find_all('td')
                text += f"{str(i+1)}. **{info[1].text}** - `{info[3].text}`\n"

            embed = Embed(
                title=f"Metas {self.names[modo]}",
                color=self.colors[modo],
                description=text
            )

            img = div.select_one("h3 img")
            embed.set_thumbnail(url=img["src"])

            #last_update = soup.select_one("div.input-group option", selected=True).text
            #embed.set_footer(text=f"Ultima atualização: {last_update}")

            await msg.delete()
            await ctx.channel.send(embed=embed)
