from discord import app_commands
import discord
import bdg
import json

__all__ = [ "DebugCommand" ]

class DebugCommand(app_commands.Group, name="debug", description="Comando Debug. (!) SOMENTTE PESSOAL AUTORIZADO"):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		super().__init__()


	@app_commands.command(name="importar_mongo", description="Importe um documento ao banco de dados")
	async def import_mongo(self, i: discord.Interaction, coleção: str, documento: str):
		try:
			doc = json.loads(documento)
		except Exception as e:
			await i.response.send_message(f":warning: | Este JSON é invalido: `{e}`", ephemeral=True)
			return

		if not isinstance(doc.get('_id'), str):
			await i.response.send_message(":warning: | O documento necessita ter um atributo `_id` e ser do tipo `str`", ephemeral=True)
			return

		id = doc['_id']
		del(doc['_id'])

		try:
			coll = self.bot.mongodb[coleção]
			coll.update_one(
				{'_id': id},
				{'$set': doc},
				upsert=True
			)
		except Exception as e:
			await i.response.send_message(f":warning: | Houve um erro ao salvar o documento: `{e}`", ephemeral=True)
			return
		
		await i.response.send_message(f":white_check_mark: | O documento com o ID `{id}` foi salvo na coleção `{coll.name}` com sucesso!", ephemeral=True)


	@app_commands.command(name="exportar_mongo", description="Exporte um documento do banco de dados")
	async def export_mongo(self, i: discord.Interaction, coleção: str, id: str):
		try:
			if not isinstance(id, str):
				raise TypeError("'id' is not an instance of 'str'")

			coll = self.bot.mongodb[coleção]
			doc = coll.find_one(id)
			if doc == None:
				raise ValueError("Document not found")

		except Exception as e:
			await i.response.send_message(f":warning: | Houve um erro ao carregar o documento: `{e}`", ephemeral=True)
			return
		
		await i.response.send_message(f":white_check_mark: | Aqui está o documento com o ID `{doc['_id']}`: ```json\n{json.dumps(doc)}```", ephemeral=True)


	@app_commands.command(name="rodar_python", description="Execute uma linha de código python")
	async def run_python(self, i: discord.Interaction, code: str):
		try:
			result = eval(code)
		except Exception as e:
			await i.response.send_message(f":warning: | Ocorreu uma excessão ao executar o código: `{e}`", ephemeral=True)
			return
		
		await i.response.send_message(f":white_check_mark: | Código executado com sucesso com o resultado: `{result}`", ephemeral=True)


	@app_commands.command(name="desligar", description="Me desliga")
	async def shutdown(self, i: discord.Interaction):
		await i.response.send_message("Desligando...", ephemeral=True)
		await self.bot.close()


	async def interaction_check(self, i: discord.Interaction) -> bool:
		return i.user.id in self.bot.config["debug_allowed"]