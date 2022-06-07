from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.context import InteractionContext
from utils import OptionTypes
from events import DefineInfo

hacker_style_dict = {
	"a": "4",
	"s": "5",
	"o": "0",
	"e": "3"
}

def define_format_command(e: DefineInfo):

	@e.slash.slash(
		name="formatar",
		description="Formate um texto de acordo com o estilo selecionado",
		options=[
			create_option(
				name="estilo",
				description="Como o texto deve ser estilizado",
				option_type=OptionTypes.STRING,
				required=True,
				choices=[
					create_choice(
						name="MAIÚSCULO",
						value="upper"
					),
					create_choice(
						name="minúsculo",
						value="lower"
					),
					create_choice(
						name="oirártnoc oA",
						value="reverted"
					),
					create_choice(
						name="E s p a ç a d o",
						value="spaced"
					),
					create_choice(
						name="H4ck3r",
						value="hacker"
					)
				]
			),
			create_option(
				name="texto",
				description="O texto a ser formatado",
				option_type=OptionTypes.STRING,
				required=True
			)
		],
		guild_ids=e.allowed_guilds["default"]
	)
	async def formatar(ctx: InteractionContext, estilo: str, texto: str):

		text = ""

		if estilo == "upper":
			text = texto.upper()

		if estilo == "lower":
			text = texto.lower()

		if estilo == "reverted":
			# Loop pelo "texto" ao contrário.
			for char in texto[len(texto) - 1: -1: -1]:
				text += char

		elif estilo == "spaced":
			chars = list(texto)
			text = " ".join(chars)

		elif estilo == "hacker":
			# Para cada caractére, use-o como chave no dicionário "hacker_style_dict",
			# ... se a chave não existe, use o próprio caractére
			texto = texto.lower()
			text = "".join([hacker_style_dict.get(char, char) for char in texto])


		await ctx.send(":speech_balloon: | " + text)