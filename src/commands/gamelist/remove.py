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

		game_index = gamelist.index_of_closest(nome_do_jogo)
		if game_index == None:
			await i.response.send_message(f":warning: | Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return

		name = gamelist.get_name(game_index)
		gamelist.remove_game(game_index)
		gamelist.save_to_mongo()
		
		await i.response.send_message(f":white_check_mark: | **{name}** removido!")