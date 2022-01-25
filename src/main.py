import discord
import pymongo
import game_list
import events
import asyncio
import json
from os import getenv
from os.path import exists
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission

# Importing commands

def load_profile(file):
    global bot_config
    global profile

    if exists(file):
        with open(file) as file:
            profile = json.loads(file.read())

    if profile.get("config", None) != None:
        if type(profile["config"]) == str: # Se a "config" for uma string, pega as configs da variavel do ambiente com este nome.
            bot_config = json.loads(getenv("BDG_CONFIG"))

        elif type(profile["config"]) == dict: # Se for um dict só carrega este dict como as configs.
            bot_config = profile["config"]

        else:
            bot_config = {}

    else:
        bot_config = {}

def connect_to_mongo_database(mongo_uri):
    global mongo_client
    global mongo_collection

    print("Conectando ao mongo database...")
    if mongo_uri != None and mongo_uri != "":
        mongo_client = pymongo.MongoClient(mongo_uri)
        mongo_collection = mongo_client["BotDusGuri"]["default"]

def instantiate_bot():
    global bot
    global slash

    print("Carregando discord client e slash commands...")
    bot = discord.ext.commands.Bot(command_prefix="/")
    slash = SlashCommand(bot, sync_commands=True)

    @bot.event
    async def on_ready():
        game = discord.Game(f"{profile.get('game', 'Online')} v{profile.get('bot_version', '404')}")
        await bot.change_presence(status=discord.Status[profile.get("status", "online").lower()], activity=game)
        print("Estou pronto!")


def build_permissions():
    print("Contruindo permissões")
    global allowed_guilds
    global default_permissions

    doc = mongo_collection.find_one({"_name": "allowed_guilds"})
    allowed_guilds = doc["allowed_guilds"]
    default_permissions = [
        create_permission(
            id=867858666525949972,
            id_type=1,
            permission=True
        ),
        create_permission(
            id=744991248284254278,
            id_type=1,
            permission=False
        )
    ]

def instantiate_gamelist():
    print("Carregando gamelist...")
    global gamelist

    gamelist = game_list.build_gamelist(mongo_collection)

def create_base_event():
    return events.BaseEvent(
        slash,
        bot,
        mongo_collection,
        profile,
        bot_config,
        allowed_guilds,
        gamelist,
        default_permissions
    )

def build_commands(base_event):
    from commands.fun.calc import CalculateCommand
    from commands.fun.choose import ChooseCommand
    from commands.fun.dice import DiceCommand
    from commands.fun.roll import RollCommand
    from commands.gl.add import AddGameCommand
    from commands.gl.game import GameCommand
    from commands.gl.icon import SetIconCommand
    from commands.gl.list import GameListCommand
    from commands.gl.name import SetNameCommand
    from commands.gl.remove import RemoveGameCommand
    from commands.gl.review import ReviewGameCommand
    from commands.gl.source import SetSourceCommand
    from commands.gl.surprise import SurpriseGameCommand
    from commands.misc.ping import PingCommand
    from commands.misc.debug import DebugCommand
    from commands.utilities.metas import MetaCommand

    print("Initializing commands...")
    CalculateCommand(base_event)
    ChooseCommand(base_event)
    DiceCommand(base_event)
    RollCommand(base_event)

    AddGameCommand(base_event)
    GameCommand(base_event)
    SetIconCommand(base_event)
    GameListCommand(base_event)
    SetNameCommand(base_event)
    RemoveGameCommand(base_event)
    ReviewGameCommand(base_event)
    SetSourceCommand(base_event)
    SurpriseGameCommand(base_event)

    PingCommand(base_event)
    DebugCommand(base_event)

    MetaCommand(base_event)

    if profile.get("send_error_to", None) != None:
        @bot.event
        async def on_slash_command_error(ctx, excep):
            user = await bot.fetch_user(profile["send_error_to"])
            await user.send(f"Houve uma exceção durante a execução do comando `{ctx.name}`.\n```\n{excep}\n```")

def build_triggers(base_event):
    from triggers.voice_join import VoiceJoinTrigger
    #from triggers.microbit import MicrobitMessageTrigger

    print("Inicializando gatilhos...")
    VoiceJoinTrigger(base_event)
    #MicrobitMessageTrigger(base_event)


def start():
    if exists("res/test_profile.json"):
        load_profile("res/test_profile.json")
    else:
        load_profile("res/profile.json")
    
    connect_to_mongo_database(bot_config.get("mongo_uri", None))
    instantiate_gamelist()
    build_permissions()
    instantiate_bot()
    base_event = create_base_event()
    build_commands(base_event)
    build_triggers(base_event)

    print("Inicializando bot...")
    bot.run(bot_config["token"])

if __name__ == "__main__":
    start()