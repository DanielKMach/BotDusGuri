
def define_voicejoin_trigger(e):

	@e.bot.event
	async def on_voice_state_update(member, before, after):
		
		# Se o usuário saiu do canal OU se moveu de canal E é o mesmo canal que antes...
		# Então retorne
		if after.channel == None or before.channel != None and before.channel.id == after.channel.id:
			return

		document = e.mongo_collection.find_one({"_name": "voice_join"})
		if document == None: return

		guild_data = document.get(str(after.channel.guild.id), None)
		if guild_data == None: return

		settings = [] # Lista objetos com as configurações e os diferentes canais para notificar
		# Cada objeto tem um Int64 'notification_channel' como o ID do canal de notificações
		# Uma String 'message' como mensagem de template quando um usuário entrar na call
		# E tem um Array de Int64 'voice_channels' como uma lista de canais de voz para notificar

		if type(guild_data) == dict: # Se lista de configurações não existe, o objeto vira uma.
			settings.append(guild_data)

		elif type(guild_data) == list: # Usar os dados da guild como lista de configurações
			settings = guild_data

		
		notification_channel = None
		template_message = ""

		# Loopar pelas configurações
		for setting in settings:
			for channel_id in setting.get("voice_channels", []):
				if after.channel.id != channel_id:
					continue

				notification_channel = e.bot.get_channel(setting.get("notification_channel", None))
				template_message = setting.get("message", "&user_nick entrou no canal de voz")

		if notification_channel == None:
			return

		template_message = template_message.replace("&user_nick", member.display_name)
		template_message = template_message.replace("&user_name", member.name)
		template_message = template_message.replace("&user_mention", member.mention)
		template_message = template_message.replace("&voice_channel", after.channel.name)

		await notification_channel.send(template_message)