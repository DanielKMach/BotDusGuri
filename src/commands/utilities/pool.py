import enum
import discord
import bdg

number_to_emoji: tuple = ( ':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:' )

class OptionsView(discord.ui.View):

	items: list[int] = []


	@property
	def button_id(self):
		return self._id

	@discord.ui.button(label="Repetir", style=discord.ButtonStyle.blurple)
	async def btn1(self, i: discord.Interaction, btn: discord.ui.Button):
		self._id = "repeat"
		self.stop()

	@discord.ui.button(label="Repetir s/ escolhido", style=discord.ButtonStyle.green)
	async def btn2(self, i: discord.Interaction, btn: discord.ui.Button):
		self._id = "repeat-without"
		self.stop()

	@discord.ui.button(label="Não repetir", style=discord.ButtonStyle.red)
	async def btn3(self, i: discord.Interaction, btn: discord.ui.Button):
		self._id = "dont-repeat"
		self.stop()


class PoolCommand(bdg.BdgCommand):

	header = {
		'name': "votacao",
		'description': "Faça uma votação no servidor!"
	}

	params = {
		'opcoes': "As opções da votação, separados por espaços"
	}

	async def on_command(self, i: discord.Interaction, opcoes: str):

		items = opcoes.split(' ')

		if len(items) < 2:
			i.response.send_message(":warning: | É necessário no mínimo 2 opções para usar este comando!")

		if len(items) > 9:
			i.response.send_message(":warning: | Opções demais! A quantidade máxima de opções é 9")

		pass