from discord import app_commands, Interaction
from bdg import BotDusGuri
from enum import Enum
from json import loads, dumps

class DebugOperation(Enum):
	EXPORTMONGO  = 0
	IMPORTMONGO  = 1
	VOICETRIGGER = 2
	SHUTDOWN     = 3

class DebugCommand(app_commands.Command):

	def __init__(self, bot: BotDusGuri):
		self.bot = bot
		super().__init__(
			name= "debug",
			description= "Comando Debug. (!) SOMENTTE PESSOAL AUTORIZADO",
			callback= self.on_command,
		)
		self.add_check(
			lambda i: i.user.id in bot.config["debug_allowed"]
		)

	async def on_command(self, i: Interaction, operação: DebugOperation, argumento: str = ""):

		if operação == DebugOperation.EXPORTMONGO:
			try:
				filter = loads(argumento)
			except Exception as exception:
				await i.response.send_message(":warning: | Não foi possível importar o filtro de pesquisa", ephemeral=True)
				return

			document = self.bot.mongodb["default"].find_one(filter)
			if document == None:
				await i.response.send_message(":warning: | Não foi possível encontrar o arquivo com este filtro", ephemeral=True)
				return

			await i.response.send_message(f":pencil: | Aqui está os dados do arquivo encontrado\n```json\n{dumps(document)}\n```", ephemeral=True)


		elif operação == DebugOperation.IMPORTMONGO:
			try:
				document = loads(argumento)
			except Exception as exception:
				await i.response.send_message(f":warning: | Este JSON é invalido! `{exception}`", ephemeral=True)
				return

			if document.get("_id") == None:
				await i.response.send_message(':warning: | Você precisa de um ID para importar um documento JSON para o Mongo!\nEx: `{"_id": "games"}`', ephemeral=True)
				return

			filter = {'_id': document['_id']}
			del(document['_id'])

			self.bot.mongodb['default'].update_one(
				filter,
				{'$set': document},
				upsert=True
			)

			await i.response.send_message(f":pencil2: | O arquivo foi salvo com o ID: `{str(filter['_id'])}`", ephemeral=True)

		elif operação == DebugOperation.VOICETRIGGER:
			await i.response.send_message("TODO")

		elif operação == DebugOperation.SHUTDOWN:
			await i.response.send_message("Desligando...", ephemeral=True)
			await self.bot.close()