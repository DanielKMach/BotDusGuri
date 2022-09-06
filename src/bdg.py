import discord
import discord.ext.commands
import pymongo.collection
import pymongo.errors
import gamelist
import random

class BotDusGuri(discord.ext.commands.Bot):

	def __init__(self):
		super().__init__(command_prefix="\\", intents=discord.Intents.all())
		self._cached_gamelist = None

	@property
	def config(self):
		return self._config
	
	@property
	def mongo_client(self):
		return self._mongo_client
	
	@property
	def mongodb(self):
		return self._mongodb


	def load_config(self, file_path: str):
		from os.path import exists
		from json import loads

		print("Carregando config...")
		if exists(file_path):
			with open(file_path) as f:
				self._config: dict[str, any] = loads(f.read())

		else:
			print(f"(!) ARQUIVO '{file_path}' NÃO FOI ENCONTRADO")
			exit()

		print(f"Config carregado.")

	def connect_to_mongo(self, mongo_uri: str):
		print("Conectando ao banco de dados...")

		from pymongo import MongoClient

		if mongo_uri != None and mongo_uri != "":
			self._mongo_client = MongoClient(mongo_uri)
			self._mongodb = self._mongo_client["BotDusGuri"]

	def get_gamelist(self, collection: pymongo.collection.Collection) -> gamelist.GameList:
		"""
		Returns the cached gamelist if the collection is the same from last request,
		otherwise loads gamelist from database and returns it
		"""

		if collection == None:
			return None

		if not self._cached_gamelist or self._cached_gamelist.collection.name != collection.name:
			self._cached_gamelist = gamelist.GameList(collection)
		
		return self._cached_gamelist

	def guild_collection(self, guild: discord.Guild) -> pymongo.collection.Collection:
		if not guild:
			return None

		return self.mongodb.get_collection(str(guild.id))

	async def load_commands(self):
		print("Carregando comandos...")
		import commands

		# Diversão
		self.tree.add_command(commands.ChooseCommand(self))
		self.tree.add_command(commands.DiceCommand(self))
		self.tree.add_command(commands.FormatCommand(self))
		self.tree.add_command(commands.RollCommand(self))

		# Gamelist
		self.tree.add_command(commands.AddGameCommand(self))
		self.tree.add_command(commands.RemoveGameCommand(self))
		self.tree.add_command(commands.ListGamesCommand(self))
		self.tree.add_command(commands.ViewGameCommand(self))
		self.tree.add_command(commands.ReviewGameCommand(self))
		self.tree.add_command(commands.SurpriseGameCommand(self))

		# Utilidades
		self.tree.add_command(commands.BrawlMetasCommand(self))
		self.tree.add_command(commands.PokegoCommand(self))
		self.tree.add_command(commands.ClearCommand(self))

		# Outros
		self.tree.add_command(commands.ReportCommand(self))
		self.tree.add_command(commands.PingCommand(self))
		self.tree.add_command(commands.DebugCommand(self))

	async def load_triggers(self):
		print("Carregando gatilhos...")
		import triggers

		await self.add_cog(triggers.VoiceJoinCog(self))

	async def sync_commands(self):
		await self.tree.sync()
		for guild in self.guilds:
			await self.tree.sync(guild=guild)

		print("Comandos sincronizados!")


	async def on_ready(self):
		await self.sync_commands()

		playing = discord.Game(f"v{self.config['version']} Online")
		await self.change_presence(activity=playing, status=discord.Status.online)

		print("Estou pronto!")

	async def on_message(self, message: discord.Message):
		if not self.user in message.mentions: return

		response = [
			"Olá! Como posso ajudar?",
			"Oi! Gostaria da minha ajuda?",
			"Me chamou?",
			"Olá mundo!"
		][random.randint(0, 3)]

		emoji = [':grinning:', ':smile:', ':grin:', ':wave:', ':call_me:'][random.randint(0, 4)]

		await message.channel.send(f"{emoji} | {response}")

	async def on_error(self, i: discord.Interaction, error: discord.app_commands.AppCommandError):

		if isinstance(error, discord.app_commands.CheckFailure):
			await i.response.send_message(":no_entry: | Você não tem permissão para executar este comando")