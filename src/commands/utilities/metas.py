from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord import Embed
from requests import request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def define_metas_command(e):

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
		"heist": 0xD65CD3,
		"siege": 0xF04F32
	}

	@e.slash.slash(
		name="meta",
		description="Mostra uma lista dos brawlers meta de cada modo de jogo",
		options=[
			create_option(
				name="modo_de_jogo",
				description="O modo de jogo dos Brawlers meta",
				option_type=SlashCommandOptionType.STRING,
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
				name="quantidade",
				description="A quantidade de Brawlers meta para visualizar",
				option_type=SlashCommandOptionType.INTEGER,
				required=False
			)
		],
		guild_ids=e.allowed_guilds["default"]
	)
	async def metas(ctx, modo_de_jogo, quantidade=10):
		msg = await ctx.send("*Adquirindo dados...* :game_die:")

		html = BeautifulSoup(
			request("GET", "https://brawlace.com/meta", cookies={"lang": "pt"}).content,
			"html.parser"
		)

		div = html.select_one(f"#gameModeData{modo_de_jogo}")
		brawlers = div.select_one(f"table tbody").find_all("tr")

		text = str()

		quantidade = max(min(quantidade, len(brawlers)), 3) # Basically clamp(quantidade, 3, len(brawlers))

		for i in range(quantidade):
			info = brawlers[i].find_all('td')
			brawler_name = info[1].text
			star_player_porcentage = info[3].text.split(' ')[0] # Formatting from '3.33 %' to '3.33'
			text += f"{str(i+1)}. **{brawler_name}** - `{star_player_porcentage}%`\n"

		embed = Embed(
			title=f"Top {str(quantidade)} - {names.get(modo_de_jogo, 'INDEFINIDO')}",
			color=colors.get(modo_de_jogo, 0xFFFFFF),
			description=text
		)

		# Setting author to be the brawl ace logo
		embed.set_author(
			name="Brawl Ace",
			url="https://brawlace.com/",
			icon_url="https://cdn.lag.one/ba/assets/images/icon.png?v=17.2"
		)

		# Getting the game mode image and defining it the thumbnail.
		img = div.select_one("h3 img")
		embed.set_thumbnail(url=img["src"])

		# Defining the subtitle
		embed.set_footer(text="(%) Porcentagem de Craque")

		# Getting last updated at time and defining it the timestamp.
		updated_at = html.select_one("div.input-group option", selected=True).text
		updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
		updated_at += timedelta(hours=-6) # Converting from GMT+6 to GMT-0

		embed.timestamp = updated_at

		await msg.edit(content="", embed=embed)
