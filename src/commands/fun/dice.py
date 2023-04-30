from discord import File, Interaction
import random
import bdg

class DiceCommand(bdg.BdgCommand):

	header = {
		'name': "dado",
		'description': "Um dado de 6 lados",
	}

	async def on_command(self, i: Interaction):

		await i.response.defer(thinking=True)

		num = random.randint(1, 6)
		dice_path = f"res/dices/d6_{num}.gif"

		await i.followup.send(f":game_die: | Rolem os dados!", file=File(dice_path))