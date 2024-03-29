from discord import Interaction
import bdg
import enum

class FormatStyle(enum.Enum):
	UPPER    = 0
	LOWER    = 1
	REVERSED = 2
	SPACED   = 3
	HACKER   = 4
	IRONIC   = 5

hacker_dict = {
	"a": "4",
	"s": "5",
	"o": "0",
	"e": "3"
}

class FormatCommand(bdg.BdgCommand):

	header = {
		'name': "formatar",
		'description': "Formate um texto de acordo com o estilo selecionado"
	}

	params = {
		'estilo': "O estilo do texto, podendo ser: UPPER, LOWER, REVERSED, SPACED, HACKER, IRONIC",
		'texto': "O texto a ser formatado no estilo indicado"
	}

	async def on_command(self, i: Interaction, estilo: FormatStyle, texto: str):
		text = ""

		if estilo == FormatStyle.UPPER:
			text = texto.upper()

		if estilo == FormatStyle.LOWER:
			text = texto.lower()

		if estilo == FormatStyle.REVERSED:
			# Loop pelo "texto" ao contrário.
			for char in texto[len(texto)-1:-1:-1]:
				text += char

		elif estilo == FormatStyle.SPACED:
			chars = list(texto)
			text = " ".join(chars)

		elif estilo == FormatStyle.HACKER:
			# Para cada caractére, use-o como chave no dicionário "hacker_style_dict",
			# ... se a chave não existe, use o próprio caractére
			text = "".join([hacker_dict.get(char.lower(), char) for char in texto])

		elif estilo == FormatStyle.IRONIC:
			# Se 'c' for par é maiúsculo, senão é minúsculo
			for c in range(len(texto)):
				char = texto[c]
				text += char.upper() if c % 2 else char.lower()

		await i.response.send_message(":speech_balloon: | " + text)