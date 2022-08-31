from discord import Embed, Interaction, TextStyle, User, app_commands, ui
from bdg import BotDusGuri

class ReportModal(ui.Modal, title="Reporte um bug"):

	where = ui.TextInput(label="Como você encontrou esse bug?")
	desc  = ui.TextInput(label="Descreva o bug", style=TextStyle.paragraph)

	def __init__(self, receiver: User):
		self.receiver = receiver
		super().__init__()

	async def on_submit(self, i: Interaction):

		embed = Embed(
			title="Um bug foi reportado",
			description=self.desc.value,
			color=0xFF2200
		).set_author(
			name=f"{i.guild.name} ({i.guild.id})",
			icon_url=i.guild.icon.url
		).add_field(
			name="Origem",
			value=self.where.value,
			inline=False
		)

		await self.receiver.send(f":beetle: | {i.user.name}#{i.user.discriminator} reportou um bug", embed=embed)
		await i.response.send_message(":+1: | Seu formulário foi enviado. Obrigado pela ajuda!", ephemeral=True)


class ReportCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name="reportar",
			description="Reporte um bug para o criador usando este comando",
			callback=self.on_command
		)

	async def on_command(self, i: Interaction):

		report = ReportModal(self.bot.application.owner)

		await i.response.send_modal(report)

