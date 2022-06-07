from lib2to3.pgen2.token import OP
from discord_slash.utils.manage_commands import create_option
from utils import OptionTypes

def define_clear_command(e):

	@e.slash.slash(
		name="limpar",
		description="Delete mensagens em sequência com este comando.",
		options=[
			create_option(
				name="quantidade",
				description="A quantidade de mensagens que você deseja excluir em sequência",
				option_type=OptionTypes.INTEGER,
				required=True
			)
		],
		guild_ids=e.allowed_guilds["default"]
	)
	async def limpar(ctx, quantidade=10):

		if not ctx.author.permissions_in(ctx.channel).manage_messages:
			await ctx.send(":no_entry_sign: | Você não tem permissão para executar este comando!")
			return

		if quantidade < 1 or quantidade > 100:
			await ctx.send(":warning: | Este valor está fora do limite, por favor tente um número entre 1 e 100")
			return

		messages = await ctx.channel.history(limit=quantidade).flatten()
		info = await ctx.send(f":anger_right: | Apagando **{quantidade}** mensagens...")

		for message in messages:
			await message.delete()

		await info.delete()
		await ctx.channel.send(f":white_check_mark: | **{quantidade}** mensagens apagadas!")
