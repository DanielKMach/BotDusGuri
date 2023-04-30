from discord import Interaction, app_commands
import bdg

class ReviewGameCommand(bdg.BdgCommand):

	header = {
		'name': "avaliar_jogo",
		'description': "Lista de Jogos - Dê uma nota e sua opinião sobre um jogo!",
	}

	async def on_command(self, i: Interaction, nome_do_jogo: str, nota: app_commands.Range[float, 0, 10], opinião: str = None):
		gamelist = self.bdg.get_gamelist(self.bdg.guild_collection(i.guild))

		game = gamelist[nome_do_jogo]
		if not game:
			await i.response.send_message(f"Não foi possível encontrar um jogo com o nome **{nome_do_jogo}**", ephemeral=True)
			return
		
		game.review(
			author= i.user.id,
			rating= nota,
			opinion= opinião
		)
		gamelist.save_to_mongo()

		await i.response.send_message(f":star: | Você avaliou **{game.name}** com **{nota}/10**!", ephemeral=True)
