from discord_slash.utils.manage_commands import create_option, create_choice, remove_all_commands
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, ButtonStyle
from discord_slash.model import SlashCommandOptionType
from json import loads, dumps

def define_debug_command(e):

	@e.slash.slash(
		name="debug",
		description="Comando Debug",
		options=[
			create_option(
				name="operação",
				description="Opções",
				option_type=SlashCommandOptionType.STRING,
				required=True,
				choices=[
					create_choice(
						name="Exportar Gamelist",
						value="exportar_gamelist"
					),
					create_choice(
						name="Importar Gamelist",
						value="importar_gamelist"
					),
					create_choice(
						name="Exportar arquivo Mongo",
						value="exportar_mongo"
					),
					create_choice(
						name="Importar arquivo Mongo",
						value="importar_mongo"
					),
					create_choice(
						name="Salvar Gamelist para o banco de dados",
						value="save_gamelist"
					),
					create_choice(
						name="Carregar Gamelist do banco de dados",
						value="load_gamelist"
					),
					create_choice(
						name="Desligar bot",
						value="desligar"
					)
				]
			),
			create_option(
				name="argumento",
				description="Argumento",
				option_type=3,
				required=False
			)
		]
	)
	async def debug(ctx, operação, argumento=""):
		if not ctx.author.id in e.bot_profile["debug_allowed"]:
			await ctx.send(":no_entry_sign: | Você não tem permissão para executar este comando")
			return

		if operação == "exportar_gamelist":
			json_obj = e.gamelist.get_json()
			await ctx.send(f":pencil: | Aqui está os dados da Gamelist\n```json\n{dumps(json_obj)}\n```")

		elif operação == "importar_gamelist":
			if argumento == "":
				await ctx.send(":warning: | Eu não posso importar um JSON vazio!")
				return

			try:
				e.gamelist.load_json(loads(argumento))
				await ctx.send(":pencil2: | JSON importado para a lista de jogos!")
			except Exception as exception:
				await ctx.send(f":warning: | Este JSON é invalido\nErro: `{exception}`")
				return

		elif operação == "exportar_mongo":
			try:
				search_filter = loads(argumento)
			except Exception as exception:
				await ctx.send(":warning: | Não foi possível importar o filtro de pesquisa")
				return

			document = e.gamelist._mongo_collection.find_one(search_filter)
			if document == None:
				await ctx.send(":warning: | Não foi possível encontrar o arquivo com este filtro")
				return

			del(document["_id"])
			await ctx.send(f":pencil: | Aqui está os dados do arquivo encontrado\n```json\n{dumps(document)}\n```")

		elif operação == "importar_mongo":
			try:
				json_obj = loads(argumento)
			except Exception as exception:
				await ctx.send(f":warning: | Este JSON é invalido\nErro: `{exception}`")
				return
			
			if type(json_obj.get("_name", None)) != str:
				await ctx.send(':warning: | Você precisa de um filtro para importar JSON para o Mongo!\nEx: `{"_name": "games"}`')

			search_filter = {"_name": json_obj["_name"]}
			del(json_obj["_name"])

			e.gamelist._mongo_collection.update_one(
				search_filter,
				{"$set": json_obj},
				upsert=True
			)

			await ctx.send(f":pencil2: | O arquivo foi salvo como `{search_filter['_name']}`")

		elif operação == "save_gamelist":
			e.gamelist.save_to_mongo()
			await ctx.send(":white_check_mark: | A Gamelist foi salva para o Mongo")

		elif operação == "load_gamelist":
			e.gamelist.load_from_mongo()
			await ctx.send(":white_check_mark: | A Gamelist foi carregada do Mongo")

		elif operação == "desligar":

			buttons = [
				create_button(
					style=ButtonStyle.red,
					label="Sim, tenho certeza",
					custom_id="sim"
				),
				create_button(
					style=ButtonStyle.green,
					label="Não, cancelar",
					custom_id="nao"
				)
			]
			action_row = create_actionrow(*buttons)

			confirm_msg = await ctx.send(":warning: | Você tem certeza que deseja me desligar?", components=[action_row])

			button_ctx = await wait_for_component(e.bot, components=action_row)
			if button_ctx.custom_id == "sim":
				print("Preparando para o desligamento")
				await confirm_msg.edit(content=":warning: | Desligando...", components=[])
				print("Removendo todos os comandos...")
				await remove_all_commands(e.bot.user.id, e.bot_config["token"], guild_ids=e.allowed_guilds["default"])
				print("Desligando...")
				await e.bot.close()
				return

			if button_ctx.custom_id == "nao":
				await confirm_msg.delete()
				return
		
		else:
			await ctx.send(":warning: | Esta opção não existe")