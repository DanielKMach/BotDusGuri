import discord
import bdg
import enum
import requests
import bs4
import datetime

class BrawlModes(enum.Enum):
	BRAWLBALL    = "brawlBall"
	SOLOSHOWDOWN = "soloShowdown"
	DUOSHOWDOWN  = "duoShowdown"
	GEMGRAB      = "gemGrab"
	BOUNTY       = "bounty"
	HOTZONE      = "hotZone"
	KNOCKOUT     = "knockout"
	HEIST        = "heist"
	SIEGE        = "siege"

names = {
	BrawlModes.BRAWLBALL: "FUTE-BRAWL",
	BrawlModes.SOLOSHOWDOWN: "COMBATE SOLO",
	BrawlModes.DUOSHOWDOWN: "COMBATE DUPLO",
	BrawlModes.GEMGRAB: "PIQUE-GEMA",
	BrawlModes.BOUNTY: "CAÇA ESTRELAS",
	BrawlModes.HOTZONE: "ZONA ESTRATÉGICA",
	BrawlModes.KNOCKOUT: "NOCAUTE",
	BrawlModes.HEIST: "ROUBO",
	BrawlModes.SIEGE: "ENCURRALADO"
}

colors = {
	BrawlModes.BRAWLBALL: 0x8CA0DF,
	BrawlModes.SOLOSHOWDOWN: 0x81D621,
	BrawlModes.DUOSHOWDOWN: 0x81D621,
	BrawlModes.GEMGRAB: 0x9B3DF3,
	BrawlModes.BOUNTY: 0x01CFFF,
	BrawlModes.HOTZONE: 0xE33C50,
	BrawlModes.KNOCKOUT: 0xF7831C,
	BrawlModes.HEIST: 0xD65CD3,
	BrawlModes.SIEGE: 0xF04F32
}

class BrawlMetasCommand(discord.app_commands.Command):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__(
			name="brawl_meta",
			description="Mostra uma lista dos brawlers meta de cada modo de jogo",
			callback=self.on_command
		)

	async def on_command(self, i: discord.Interaction, modo: BrawlModes, top: int = 10):

		await i.response.defer(thinking=True)

		data = self.get_metas(modo, top)
		desc = str()

		for brawler in data['brawlers']:
			desc += "{rank}. **{name}** - `{star}%`\n".format(**brawler)

		embed = discord.Embed(
			title=f"Top {top} - {names[modo]}",
			color=colors[modo],
			description=desc
		)

		# Definindo o autor como o Brawl Ace
		embed.set_author(
			name="Brawl Ace",
			url="https://brawlace.com/meta",
			icon_url="https://brawlace.com/assets/images/icon.png?v=22.87"
		)

		# Pegando o ícone do modo de jogo e definindo-o como a thumbnail
		embed.set_thumbnail(url=data['icon'])

		# Definindo legenda
		embed.set_footer(text="(%) Porcentagem de Craque")

		# definindo como timestamp como tempo da ultima atualização
		embed.timestamp = data['last_update']

		await i.followup.send(embed=embed)

	def get_metas(self, mode: BrawlModes, count: int = 10) -> dict[str, any]:

		html = bs4.BeautifulSoup(requests.get("https://brawlace.com/meta", cookies={"lang": "pt"}).content, "html.parser")
		div = html.select_one(f"#gameModeData{mode.value}")
		data = {}

		# Pegando icone do modo de jogo
		data['icon'] = div.select_one("h3 img")['src']

		# Pegando o tempo da ultima atualização
		last_update = html.select_one("div.input-group option", selected=True).text
		last_update = datetime.datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
		last_update -= datetime.timedelta(hours=7) # Convertendo de UTC+7 para UTC+0

		data['last_update'] = last_update

		# Definindo brawlers
		data['brawlers'] = []

		brawlers = div.select_one(f"table tbody").find_all("tr")

		count = sorted((3, count, len(brawlers)))[1] # Mesma coisa que .clamp()
		for i in range(count):
			info = {}

			brawler = brawlers[i].find_all('td')
			info['rank'] = i + 1
			info['name'] = brawler[1].text
			info['star'] = float(brawler[3].text[0:-2]) # Formatando de '3.33 %' para 3.33

			data['brawlers'].append(info)
		
		return data
