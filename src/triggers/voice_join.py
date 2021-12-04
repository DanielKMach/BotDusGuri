
class VoiceJoinTrigger:

    def __init__(self, e):

        @e.bot.event
        async def on_voice_state_update(member, before, after):
            if before.channel == None and after.channel != None:
                voice_channel = None
                notification_channel = None
                message = ""

                doc = e.mongo_collection.find_one({"_name": "voice_join"})
                settings = doc[str(after.channel.guild.id)]

                for channel_id in settings.get("voice_channels", []):
                    if after.channel.id == channel_id:
                        voice_channel = e.bot.get_channel(channel_id)
                notification_channel = e.bot.get_channel(settings.get("notification_channel", None))
                message = settings.get("message", "&user_nick entrou no canal de voz")

                if voice_channel == None or notification_channel == None:
                    return

                message = message.replace("&user_nick", member.display_name)
                message = message.replace("&user_name", member.name)
                message = message.replace("&user_mention", member.mention)
                message = message.replace("&voice_channel", after.channel.name)

                await notification_channel.send(message)