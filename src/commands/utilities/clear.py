from discord import Interaction, app_commands
import bdg

class ClearCommand(bdg.BdgCommand):

	header = {
		'name': "limpar",
		'description': "Exclua mensagens em sequência com este comando."
	}

	params = {
		'quantidade': "A quantidade de mensagens que você deseja limpar"
	}

	@app_commands.checks.has_permissions(manage_messages=True)
	async def on_command(self, i: Interaction, quantidade: app_commands.Range[int, 1, 100]):

		# Clamp não existe então copiei essa gambiarra do stackoverflow
		quantidade = sorted((1, quantidade, 100))[1]

		messages = [ msg async for msg in i.channel.history(limit=quantidade) ]

		await i.response.defer(ephemeral=True)

		for message in messages:
			await message.delete()

		await i.followup.send(f":white_check_mark: | **{quantidade}** mensagens apagadas!", ephemeral=True)