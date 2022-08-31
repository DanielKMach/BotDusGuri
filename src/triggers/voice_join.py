from discord import Member, VoiceState
from discord.ext import commands
from bdg import BotDusGuri

class VoiceJoinCog(commands.Cog, name='VoiceJoin'):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):

		# Se o usuário saiu do canal OU se moveu de canal E é o mesmo canal que antes, retorne
		# Resumindo.. continue o código se o usuário entrou em um canal de voz
		if after.channel == None or before.channel != None and before.channel.id == after.channel.id:
			return

		document = self.bot.guild_collection(member.guild).find_one({"_id": "voice_join"})
		if document == None: return

		nodes = []

		if type(document.get('nodes')) == list:
			nodes = document['nodes']

		elif type(document.get('nodes')) == dict:
			nodes.append(document['nodes'])

		else:
			nodes.append(document)
		
		notification_channel = None
		template_message = ""

		# Loopar pelas configurações
		for node in nodes:
			for channel_id in node.get("voice_channels", []):
				if after.channel.id != channel_id:
					continue

				notification_channel = self.bot.get_channel(node.get("notification_channel", None))
				template_message = node.get("message", "&user_nick entrou no canal de voz")

		if notification_channel == None:
			return

		template_message = template_message.replace("&user_nick", member.display_name)
		template_message = template_message.replace("&user_name", member.name)
		template_message = template_message.replace("&user_mention", member.mention)
		template_message = template_message.replace("&voice_channel", after.channel.name)

		await notification_channel.send(template_message)