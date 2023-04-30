import discord
import bdg

__all__ = [ "PingCommand" ]

class PingCommand(bdg.BdgCommand):

	header = {
		'name': "ping",
		'description': "A latência entre eu e você!"
	}

	async def on_command(self, i: discord.Interaction):
		await i.response.send_message(f":ping_pong: | O ping atual é de **{int(self.bdg.latency * 1000)}ms**", ephemeral=True)