from discord import app_commands, ui, ButtonStyle, Interaction
from bdg import BotDusGuri
from random import randint

class ChooseView(ui.View):

	@property
	def button_id(self):
		return self._id

	@ui.button(label="Repetir", style=ButtonStyle.blurple)
	async def btn1(self, i: Interaction, btn: ui.Button):
		self._id = "repeat"
		self.stop()

	@ui.button(label="Repetir s/ escolhido", style=ButtonStyle.green)
	async def btn2(self, i: Interaction, btn: ui.Button):
		self._id = "repeat-without"
		self.stop()

	@ui.button(label="Não repetir", style=ButtonStyle.red)
	async def btn3(self, i: Interaction, btn: ui.Button):
		self._id = "dont-repeat"
		self.stop()


class ChooseCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name="escolher",
			description="Escolha entre 2 ou mais opções",
			callback=self.on_command
		)

	async def on_command(self, i: Interaction, escolhas: str):

		choices = escolhas.split(" ")

		if len(choices) <= 1:
			await i.response.send_message(":warning: | Você precisa especificar 2 ou mais opções", ephemeral=True)
			return

		while True:
			chosen = choices[randint(0, len(choices) - 1)]

			view = ui.View()
			msg = f":slot_machine: | O escolhido foi... **{chosen}**!"

			if len(choices) > 1:
				view = ChooseView()
				msg += f"\n*...de {len(choices)} itens.*"

			followup_msg = None
			if not i.response.is_done():
				await i.response.send_message(msg, view=view)
			else:
				followup_msg = await i.followup.send(msg, view=view, wait=True)

			if len(choices) <= 1:
				return

			# Espera até usuário responder
			timedout = await view.wait()
			
			# Edita mensagem e remove os componentes
			if followup_msg != None:
				await followup_msg.edit(view=None)
			else:
				await i.edit_original_response(view=None)

			if view.button_id == "dont-repeat" or timedout:
				return

			if view.button_id == "repeat-without":
				choices.remove(chosen)