from discord import Interaction
import bdg

class RemoveGameCommand(bdg.BdgCommand):

	header = {
		'name': "remover_jogo",
		'description': "Lista de Jogos - Remova um jogo da lista",
	}
	
	async def on_command(self, i: Interaction, nome_do_jogo: str):

		gamelist = self.bdg.get_gamelist(self.bdg.guild_collection(i.guild))

		index = gamelist.index_of(nome_do_jogo)
		if index == None:
			await i.response.send_message(f":warning: | Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return

		game = gamelist.delete_game(index)
		gamelist.save_to_mongo()
		
		await i.response.send_message(f":white_check_mark: | **{game.name}** removido!", ephemeral=True)