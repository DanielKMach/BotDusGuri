import discord
import asyncio
#import threading
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from random import randint
from os import getenv

voice_channel_id = 744991248284254283
text_channel_id = 786810994630328330

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)


#def timer():
#     time.sleep(5)
#     print("Shutting down bot")
#     await client.close()
#     time.sleep(20)
#     print("Turning on bot")
#     client.run("Nzg2NzkxOTQ1NjkwOTM5NDEz.X9LjGQ.rGAJ1XnpL5LO0Lv7iuC70cz1ZLo")



@client.event
async def on_ready():
    print("I'm ready")
    global text_channel
    text_channel = client.get_channel(text_channel_id)
    #threading._start_new_thread(timer())
    #game = discord.Game("Testando uns baga")
    #await client.change_presence(status=discord.Status.idle, activity=game)
    game = discord.Game("Online")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == None and after.channel != None and after.channel.id == voice_channel_id:
        await text_channel.send("***" + member.display_name + "*** entrou no canal de voz")


@slash.slash(
    name="roleta",
    description="Um número aleatório!",
    options=[
        create_option(
            name="mínimo",
            description="Valor mínimo para sortear",
            option_type=4,
            required=False
        ),
        create_option(
            name="máximo",
            description="Valor máximo para sortear",
            option_type=4,
            required=False
        ),
    ]
)
async def roleta(ctx, mínimo=1, máximo=10):
    await ctx.send(f"A roleta entre `{mínimo}` e `{máximo}` deu... **{randint(mínimo, máximo)}**!")


@slash.slash(
    name="calculo",
    description="Uma calculadora em forma de chat!",
    options=[
        create_option(
            name="espressão",
            description="Uma espressão matemática",
            option_type=3,
            required=True
        ),
    ]
)
async def calculo(ctx, espressão):
    await ctx.send(f"`{espressão}` = **{eval(espressão)}**")


@slash.slash(
    name="ping",
    description="A latência entre eu e você"
)
async def ping(ctx):
    await ctx.send(f"O ping atual é de {str(int(client.latency * 1000))}ms")


client.run(getenv("BDG_TOKEN"))
