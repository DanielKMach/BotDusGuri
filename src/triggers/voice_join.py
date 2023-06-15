import discord
import discord.ext.commands
import bdg

class VoiceJoinCog(discord.ext.commands.Cog, name='VoiceJoin'):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot

	@discord.ext.commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

		# Se o usuário saiu do canal OU se moveu de canal E é o mesmo canal que antes, retorne
		# Resumindo.. continue o código se o usuário entrou em um canal de voz
		if after.channel == None or before.channel != None and before.channel.id == after.channel.id:
			return

		document = self.bot.guild_collection(member.guild).find_one({'_id': "voice_join"})
		if document == None or not document.get('active', True):
			return

		nodes: list[dict] = []

		if isinstance(n := document.get('nodes'), list):
			nodes = n

		if isinstance(n := document.get('nodes'), dict):
			nodes.append(n)

		else:
			nodes.append(document)
		
		notification_channel = None
		template_message = ""

		# Loopar pelas configurações
		for node in nodes:
			for channel_id in node.get("voice_channels", []):
				if after.channel.id != int(channel_id):
					continue

				notification_channel = self.bot.get_channel(int(node.get("notification_channel", 0)))
				template_message = node.get("message", "&user_nick entrou no canal de voz")

		if notification_channel == None:
			return

		template_message = template_message.replace("&user_nick", member.display_name)
		template_message = template_message.replace("&user_name", member.name)
		template_message = template_message.replace("&user_mention", member.mention)
		template_message = template_message.replace("&voice_channel", after.channel.name)

		await notification_channel.send(template_message)