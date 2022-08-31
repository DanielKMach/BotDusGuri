import bdg
from discord import app_commands, Interaction
import random

class RollCommand(app_commands.Command):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "roleta",
			description= "Um número aleatório entre o mínimo e o máximo",
			callback= self.on_command
		)

	@app_commands.describe(
		mínimo="Valor mínimo a ser sorteado",
		máximo="Valor máximo a ser sorteado"
	)
	async def on_command(self, i: Interaction, mínimo: int = 1, máximo: int = 10):
		await i.response.send_message(f":game_die: | A roleta entre `{mínimo}` e `{máximo}` deu... **{random.randint(mínimo, máximo)}**!")