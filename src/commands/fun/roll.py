from discord import app_commands, Interaction
import random
import bdg

class RollCommand(bdg.BdgCommand):

	header = {
		'name': "roleta",
		'description': "Um número aleatório entre o mínimo e o máximo"
	}

	params = {
		'mínimo': "O valor mínimo a ser sorteado",
		'máximo': "O valor máximo a ser sorteado"
	}
	
	async def on_command(self, i: Interaction, mínimo: int = 1, máximo: int = 10):
		await i.response.send_message(f":game_die: | A roleta entre `{mínimo}` e `{máximo}` deu... **{random.randint(mínimo, máximo)}**!")