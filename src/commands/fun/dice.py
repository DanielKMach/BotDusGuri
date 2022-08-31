from discord import app_commands, File, Interaction
from bdg import BotDusGuri
from random import randint

class DiceCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name="dado",
			description="Um dado de 6 lados",
			callback=self.on_command
		)

	async def on_command(self, i: Interaction):

		await i.response.defer(thinking=True)

		num = randint(1, 6)
		dice_path = f"res/dices/dice_{num}.gif"

		await i.followup.send(file=File(dice_path))