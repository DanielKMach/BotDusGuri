from discord import Interaction, app_commands
from bdg import BotDusGuri

class RemoveGameCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "remover_jogo",
			description= "Lista de Jogos - Remova um jogo da lista",
			callback= self.on_command
		)
	
	async def on_command(self, i: Interaction, nome_do_jogo: str):

		gamelist = self.bot.get_gamelist(self.bot.guild_collection(i.guild))

		index = gamelist.index_of(nome_do_jogo)
		if index == None:
			await i.response.send_message(f":warning: | Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return

		game = gamelist.delete_game(index)
		gamelist.save_to_mongo()
		
		await i.response.send_message(f":white_check_mark: | **{game.name}** removido!", ephemeral=True)