from discord import Embed, Interaction, TextStyle, User, ui
import bdg

__all__ = [ "ReportModal", "ReportCommand" ]

class ReportModal(ui.Modal, title="Reporte um bug"):

	where = ui.TextInput(label="Como você encontrou esse bug?")
	desc  = ui.TextInput(label="Descreva o bug", style=TextStyle.paragraph)

	def __init__(self, receiver: User):
		self.receiver = receiver
		super().__init__()

	async def on_submit(self, i: Interaction):

		embed = Embed(
			title=self.where.value,
			description=self.desc.value,
			color=0xFF2200
		).set_author(
			name=f"{i.guild.name} ({i.guild.id})",
			icon_url=i.guild.icon.url
		)

		await self.receiver.send(f":beetle: | {i.user.name}#{i.user.discriminator} reportou um bug", embed=embed)
		await i.response.send_message(":+1: | Seu formulário foi enviado. Obrigado pela ajuda!", ephemeral=True)


class ReportCommand(bdg.BdgCommand):

	header = {
		'name': "reportar_bug",
		'description': "Reporte um bug para o criador usando este comando."
	}

	async def on_command(self, i: Interaction):
		report = ReportModal(self.bdg.application.owner)
		await i.response.send_modal(report)