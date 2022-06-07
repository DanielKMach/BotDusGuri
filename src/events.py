
class DefineInfo:

	def __init__(self, slash, bot, mongo_collection, bot_profile, bot_config, allowed_guilds, gamelist, default_permissions):
		self.slash = slash
		self.bot = bot
		self.mongo_collection = mongo_collection
		self.bot_profile = bot_profile
		self.bot_config = bot_config
		self.allowed_guilds = allowed_guilds
		self.gamelist = gamelist
		self.default_permissions = default_permissions