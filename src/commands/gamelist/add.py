from discord import Interaction, app_commands, ui
from bdg import BotDusGuri
from gamelist import GameList

class GameModal(ui.Modal, title="Adicionar um jogo"):

	name =   ui.TextInput(label="Nome do jogo", min_length=3, max_length=30)
	icon =   ui.TextInput(label="Ícone do jogo (url)", min_length=3, required=False)
	source = ui.TextInput(label="Link de download (url)", min_length=3, required=False)

	def __init__(self, gamelist: GameList):
		self.gamelist = gamelist
		super().__init__()

	async def on_submit(self, i: Interaction):
		self.gamelist.create_game(
			name= self.name.value,
			icon_url= self.icon.value,
			source= self.source.value,
			added_by= i.user.id
		)
		self.gamelist.save_to_mongo()

		await i.response.send_message(content=f":white_check_mark: | **{self.name.value}** adicionado com sucesso!", ephemeral=True)
		self.stop()

class AddGameCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "adicionar_jogo",
			description= "Lista de Jogos - Adicione um jogo à lista",
			callback= self.on_command
		)
	
	async def on_command(self, i: Interaction):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))
		modal = GameModal(gamelist)

		await i.response.send_modal(modal)