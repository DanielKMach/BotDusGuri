import discord
import asyncio

voice_channel_id = 744991248284254283
text_channel_id = 786810994630328330

client = discord.Client()

@client.event
async def on_ready():
     print("I'm ready")
     global text_channel
     text_channel = client.get_channel(text_channel_id)

@client.event
async def on_voice_state_update(member, before, after):
     if before.channel == None and after.channel != None and after.channel.id == voice_channel_id:
          await text_channel.send("***" + member.name + "** entrou no canal de voz*")

client.run("Nzg2NzkxOTQ1NjkwOTM5NDEz.X9LjGQ.rGAJ1XnpL5LO0Lv7iuC70cz1ZLo")