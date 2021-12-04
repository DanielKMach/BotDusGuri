import discord
import pymongo
import game_list
import events
import asyncio
import json
from os import getenv
from os.path import exists
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission, remove_all_commands

# Importing commands

def load_profile(file):
    global bot_config
    global profile

    if exists(file):
        with open(file) as file:
            profile = json.loads(file.read())

    if profile.get("config", None) != None:
        if type(profile["config"]) == str:
            bot_config = json.loads(getenv("BDG_CONFIG"))

        elif type(profile["config"]) == dict:
            bot_config = profile["config"]

        else:
            bot_config = {}

    else:
        bot_config = {}

def connect_to_mongo_database(mongo_uri):
    global mongo_client
    global mongo_collection

    print("Connecting to mongo database...")
    if mongo_uri != None and mongo_uri != "":
        mongo_client = pymongo.MongoClient(mongo_uri)
        mongo_collection = mongo_client["BotDusGuri"]["default"]

def instantiate_bot():
    global bot
    global slash

    print("Loading discord client and slash commands...")
    bot = discord.ext.commands.Bot(command_prefix="/")
    slash = SlashCommand(bot, sync_commands=True)

    @bot.event
    async def on_ready():
        game = discord.Game(profile.get("game", "Online"))
        await bot.change_presence(status=discord.Status[profile.get("status", "online").lower()], activity=game)
        print("I'm ready")


def build_permissions():
    print("Contruindo permissões")
    global allowed_guilds
    global default_permissions

    allowed_guilds = [744991248284254278]
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
    print("Building gamelist...")
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

def remove_all_commands(bot):
    bot.remove_command("calculo")
    bot.remove_command("escolher")
    bot.remove_command("roleta")
    bot.remove_command("adicionar_jogo")
    bot.remove_command("ver_jogo")
    bot.remove_command("definir_icone")
    bot.remove_command("lista_de_jogos")
    bot.remove_command("definir_nome")
    bot.remove_command("remover_jogo")
    bot.remove_command("avaliar_jogo")
    bot.remove_command("definir_fonte")
    bot.remove_command("sortear_jogo")
    bot.remove_command("ping")
    bot.remove_command("debug")

def build_commands(base_event):
    from commands.fun.calc import CalculateCommand
    from commands.fun.choose import ChooseCommand
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

    print("Initializing commands...")
    CalculateCommand(base_event)
    ChooseCommand(base_event)
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

def build_triggers(base_event):
    from triggers.voice_join import VoiceJoinTrigger

    print("Inicializando gatilhos...")
    VoiceJoinTrigger(base_event)


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

    print("Initializing bot...")
    bot.run(bot_config["token"])

async def close_bot(bot):
    #remove_all_commands(bot)
    await bot.close()




if __name__ == "__main__":
    start()