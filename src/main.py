import discord
import pymongo
import gamelist as gl
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

	print("Carregando perfil...")
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

	print(f"Perfil '{profile.get('name', 'unknown')}' carregado.")

def connect_to_mongo_database(mongo_uri):
	global mongo_client
	global mongo_collection

	print("Conectando ao banco de dados...")
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
	if doc == None:
		emergency_database_setup()

	allowed_guilds = doc.get("allowed_guilds", None)
	if allowed_guilds == None:
		emergency_database_setup()

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

	gamelist = gl.build_gamelist(mongo_collection)

def create_defineinfo():
	return events.DefineInfo(
		slash,
		bot,
		mongo_collection,
		profile,
		bot_config,
		allowed_guilds,
		gamelist,
		default_permissions
	)

def build_commands(defineinfo):
	print("Inicializando comandos...")
	import commands

	commands.define_calculate_command(defineinfo)
	commands.define_choose_command(defineinfo)
	commands.define_dice_command(defineinfo)
	commands.define_format_command(defineinfo)
	commands.define_roll_command(defineinfo)

	commands.define_addgame_command(defineinfo)
	commands.define_viewgame_command(defineinfo)
	commands.define_viewlist_command(defineinfo)
	commands.define_removegame_command(defineinfo)
	commands.define_reviewgame_command(defineinfo)
	commands.define_seticon_command(defineinfo)
	commands.define_setname_command(defineinfo)
	commands.define_setsource_command(defineinfo)
	commands.define_sortgames_command(defineinfo)

	commands.define_clear_command(defineinfo)
	commands.define_metas_command(defineinfo)
	commands.define_ping_command(defineinfo)

	commands.define_debug_command(defineinfo)

	if profile.get("send_error_to_owner", False):
		@bot.event
		async def on_slash_command_error(ctx, excep):
			user = await bot.fetch_user(profile["owner"])
			await user.send(f"Ocorreu um erro durante a execução do comando `{ctx.name}`.\n```\n{excep}\n```")

def build_triggers(defineinfo):
	print("Inicializando gatilhos...")
	import triggers

	triggers.define_voicejoin_trigger(defineinfo)
	#triggers.define_microbit_trigger(defineinfo)

def emergency_database_setup():
	print("OCORREU UM ERRO DURANTE O CARREGAMENTO DO BANCO DE DADOS")
	print("INICIALIZANDO RESET DE EMERGÊNCIA DO BANCO DE DADOS")

	document = {
		"_name":"allowed_guilds",
		"allowed_guilds": {
			"default":[],
			"gamelist":[]
		}
	}

	mongo_collection.insert_one(document)

	print("Setup concluído. Por favor reinicie a aplicação")
	exit()

def start():
	if exists("res/test_profile.json"):
		load_profile("res/test_profile.json")
	else:
		load_profile("res/profile.json")
	
	connect_to_mongo_database(bot_config.get("mongo_uri", None))
	instantiate_gamelist()
	build_permissions()
	instantiate_bot()
	defineinfo = create_defineinfo()
	build_commands(defineinfo)
	build_triggers(defineinfo)

	print("Inicializando bot...")
	bot.run(bot_config["token"])

if __name__ == "__main__":
	start()