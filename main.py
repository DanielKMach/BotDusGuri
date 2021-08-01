import discord
import asyncio
import json
import math
from random import randint
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from os import getenv, environ
from ast import literal_eval
from game_list import GameList

voice_channel_id = 744991248284254283
text_channel_id = 786810994630328330

bot = discord.ext.commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True)
game_list: GameList
text_channel: discord.TextChannel
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


def save_gamelist():
    global game_list
    with open("games.json", mode="w", encoding="UTF-8") as file:
        file.write(json.dumps({"games": game_list._games}, indent=4, sort_keys=True))

def load_gamelist():
    global game_list
    with open("games.json", mode="r", encoding="UTF-8") as file:
        games = json.loads(file.read()).get("games", [])
    game_list = GameList(games=games)

load_gamelist()



@bot.event
async def on_ready():
    global text_channel
    text_channel = bot.get_channel(text_channel_id)

    #game = discord.Game("Testando uns baga")
    #await bot.change_presence(status=discord.Status.idle, activity=game)
    game = discord.Game("Online")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("I'm ready")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == None and after.channel != None and after.channel.id == voice_channel_id:
        await text_channel.send("***" + member.display_name + "*** entrou no canal de voz")


@slash.slash(
    name="roleta",
    description="Um número aleatório!",
    options=[
        create_option(
            name="mínimo",
            description="Valor mínimo para sortear",
            option_type=4,
            required=False
        ),
        create_option(
            name="máximo",
            description="Valor máximo para sortear",
            option_type=4,
            required=False
        ),
    ],
    guild_ids=allowed_guilds
)
async def roleta(ctx, mínimo=1, máximo=10):
    await ctx.send(f":game_die: | A roleta entre `{mínimo}` e `{máximo}` deu... **{randint(mínimo, máximo)}**!")


@slash.slash(
    name="calculo",
    description="Uma calculadora em forma de chat!",
    options=[
        create_option(
            name="expressão",
            description="Uma expressão matemática",
            option_type=3,
            required=True
        ),
    ],
    guild_ids=allowed_guilds
)
async def calculo(ctx, expressão):
    try:
        solution = eval(expressão)
    except:
        await ctx.send(":warning: | Desculpa mas eu não consigo calcular isto")
        return

    await ctx.send(f":abacus: | `{expressão}` = **{str(solution)}**")


@slash.slash(
    name="ping",
    description="A latência entre eu e você",
    guild_ids=allowed_guilds
)
async def ping(ctx):
    await ctx.send(f":ping_pong: | O ping atual é de **{str(int(bot.latency * 1000))}ms**")


@slash.slash(
    name="lista_de_jogos",
    description="Envia a lista de jogos para jogar",
    options=[
        create_option(
            name="pesquisar",
            description="Um pedaço ou um nome usado para facilitar a visualização",
            option_type=3,
            required=False
        )
    ],
    guild_ids=allowed_guilds
)
async def lista_de_jogos(ctx, pesquisar=""):
    message = ""
    game_names = game_list.get_name_list()
    game_ratings = game_list.get_rating_median_list()

    if len(game_names) == 0:
        await ctx.send("Não existe jogos na lista")
        return

    for i in range(len(game_names)):
        message += f"{game_names[i]} - "
        if game_ratings[i] != None:
            message += f"`{game_ratings[i]}/10`"
        else:
            message += "`Sem avaliações`"
        message += "\n"

    list_embed = discord.Embed(
        title="Jogos na Lista",
        description=message,
        color=0x0090eb
    )

    await ctx.send(":scroll: | Aqui está a lista de jogos disponiveis para jogar", embed=list_embed)

@slash.slash(
    name="ver_jogo",
    description="Veja mais detalhes sobre um jogo especifico",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome do jogo para ver mais sobre ele",
            option_type=3,
            required=True,
            choices=game_list.get_choices()
        )
    ],
    guild_ids=allowed_guilds
)
async def ver_jogo(ctx, nome_do_jogo):
    game_index = game_list.index_of(nome_do_jogo)

    game_embed = discord.Embed(
        title=game_list.get_name(game_index),
        color=0x00b934
    )

    icon = game_list.get_icon(game_index)
    if icon != "":
        print("There is icon")
        game_embed.set_thumbnail(url=icon+".png")

    source = game_list.get_source(game_index)
    if source != None:
        game_embed.url = source

    ratings = game_list.get_ratings(game_index)
    if len(ratings) != 0:
        ratings_text = ""
        for rating in ratings:
            rating_author = await bot.fetch_user(rating['author'])
            ratings_text += f"{rating_author.mention} - `{rating['rating']}/10`"
            if rating.get("opinion", None) != None:
                ratings_text += f" *\"{rating['opinion']}\"*"
            ratings_text += "\n"

        game_embed.add_field(
            name=f":star: | Avaliações ({game_list.get_rating_median(game_index)}/10)",
            value=ratings_text,
            inline=False
        )

    await ctx.send(f":bookmark_tabs: | Aqui estão algumas informações sobre **{game_list.get_name(game_index)}**", embed=game_embed)

@slash.slash(
    name="adicionar_jogo",
    description="Adiciona um jogo",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome do jogo que você deseja adicionar",
            option_type=3,
            required=True
        )
    ],
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def adicionar_jogo(ctx, nome_do_jogo):
    game_list.create_game(
        name=nome_do_jogo
    )
    save_gamelist()
    await ctx.send(f":white_check_mark: | **{nome_do_jogo}** adicionado com sucesso!")

    await slash.sync_all_commands()

@slash.slash(
    name="remover_jogo",
    description="Remove um jogo",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome do jogo que você deseja remover",
            option_type=3,
            required=True,
            choices=game_list.get_choices()
        )
    ],
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def remover_jogo(ctx, nome_do_jogo):
    game_list.remove_game(
        game_list.index_of(nome_do_jogo)
    )
    save_gamelist()
    await ctx.send(f":white_check_mark: | **{nome_do_jogo}** removido!")

    await slash.sync_all_commands()

@slash.slash(
    name="avaliar_jogo",
    description="Avalie um jogo!",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome do jogo que você deseja avaliar",
            option_type=3,
            required=True,
            choices=game_list.get_choices()
        ),
        create_option(
            name="nota",
            description="A Nota do jogo de `0` a `10`",
            option_type=3,
            required=True
        ),
        create_option(
            name="opinião",
            description="A sua opinião sobre o jogo",
            option_type=3,
            required=False
        )
    ],
    guild_ids=allowed_guilds
)
async def avaliar_jogo(ctx, nome_do_jogo, nota, opinião=None):
    try:
        nota = float(nota)
        nota = max(min(nota, 10), 0)
    except:
        await ctx.send(":warning: | Esta nota é inválida")
        return
    
    game_list.rate_game(
        game_list.index_of(nome_do_jogo), ctx.author.id, nota, opinion=opinião
    )
    save_gamelist()
    await ctx.send(f":star: | Você avaliou o jogo **{nome_do_jogo}** com `{str(nota)}/10`!")

@slash.slash(
    name="definir_fonte",
    description="Define um link como a fonte de um jogo",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome do jogo para definir a fonte",
            option_type=3,
            required=True,
            choices=game_list.get_choices()
        ),
        create_option(
            name="fonte",
            description="Um link da internet, provavelmente levando ao Google Play",
            option_type=3,
            required=True
        )
    ],
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def definir_fonte(ctx, nome_do_jogo, fonte):
    game_list.set_source(game_list.index_of(nome_do_jogo), fonte.lower())
    
    await ctx.send(f":link: | Definido `{fonte.lower()}` como a fonte de **{game_list.get_name(game_list.index_of(nome_do_jogo))}**")
    save_gamelist()


@slash.slash(
    name="definir_icone",
    description="Define um link como o ícone de um jogo",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome do jogo para definir o ícone",
            option_type=3,
            required=True,
            choices=game_list.get_choices()
        ),
        create_option(
            name="link",
            description="Um link da internet, provavelmente levando ao Google Play",
            option_type=3,
            required=True
        )
    ],
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def definir_icone(ctx, nome_do_jogo, link):
    game_list.set_icon(game_list.index_of(nome_do_jogo), link.lower())

    await ctx.send(f":link: | Definido ícone de **{game_list.get_name(game_list.index_of(nome_do_jogo))}**")
    save_gamelist()


@slash.slash(
    name="definir_nome",
    description="Renomeie algum jogo que você nomeou errado",
    options=[
        create_option(
            name="nome_do_jogo",
            description="O nome atual do jogo para ser renomeado",
            option_type=3,
            required=True,
            choices=game_list.get_choices()
        ),
        create_option(
            name="novo_nome",
            description="O novo nome do jogo",
            option_type=3,
            required=True
        )
    ],
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def definir_nome(ctx, nome_do_jogo, novo_nome):
    game_index = game_list.index_of(nome_do_jogo)

    old_name = game_list.get_name(game_index)
    game_list.set_name(game_index, novo_nome)

    await ctx.send(f":pencil: | **{old_name}** agora se chama **{game_list.get_name(game_index)}**!")
    save_gamelist()

    await slash.sync_all_commands()

@slash.slash(
    name="sortear_jogo",
    description="Sorteie um jogo aleatório que ainda não foi avaliado",
    guild_ids=allowed_guilds
)
async def sortear_jogo(ctx):
    games = game_list.get_name_list()
    games_to_sort = []
    for game in games:
        if game_list.get_rating_median(game_list.index_of(game)) == None:
            games_to_sort.append(game)

    if len(games_to_sort) == 0:
        await ctx.send(":warning: | Todos os jogos da lista já foram avaliados")
        return

    random_game = games_to_sort[randint(0, len(games_to_sort) - 1)]
    await ctx.send(f":tada: | O jogo sorteado é... ||**{random_game.upper()}!**||")

@slash.slash(
    name="desligar",
    description="Este comando irá me desligar",
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def desligar(ctx):
    buttons = [
        create_button(
            style=ButtonStyle.red,
            label="Sim, tenho certeza",
            custom_id="842efac9-2ffd-4d7e-8eb0-f60a183522ec"
        ),
        create_button(
            style=ButtonStyle.green,
            label="Não, cancelar",
            custom_id="504bf7f9-3441-4ecb-b16b-4bfd52b5b4bb"
        )
    ]
    action_row = create_actionrow(*buttons)

    confirm_msg = await ctx.send(":warning: | Você tem certeza que deseja me desligar?", components=[action_row])

    button_ctx: ComponentContext = await wait_for_component(bot, components=action_row)
    if button_ctx.custom_id == "842efac9-2ffd-4d7e-8eb0-f60a183522ec":
        await confirm_msg.delete()
        await ctx.send(":warning: | Desligando...")
        await bot.close()
        return

    if button_ctx.custom_id == "504bf7f9-3441-4ecb-b16b-4bfd52b5b4bb":
        await confirm_msg.delete()
        return


@slash.slash(
    name="arquivos",
    description="Comando para gerenciar os arquivos",
    options=[
        create_option(
            name="operação",
            description="Opções para gerenciar os arquivos de armazenamento de dados",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="Exportar",
                    value="exportar"
                ),
                create_choice(
                    name="Importar",
                    value="importar"
                )
            ]
        ),
        create_option(
            name="json_obj",
            description="O documento JSON que você deseja importar",
            option_type=3,
            required=False
        )
    ],
    guild_ids=allowed_guilds
)
@slash.permission(
    guild_id=allowed_guilds[0],
    permissions=default_permissions
)
async def arquivos(ctx, operação, json_obj=""):
    global game_list
    if operação == "exportar":
        load_gamelist()
        await ctx.send(f":pencil: | Aqui está os meus dados\n```json\n{json.dumps({'games': game_list._games}, indent=0, sort_keys=True)}\n```")
        return

    if operação == "importar":
        if json_obj == "":
            await ctx.send(":warning: | Eu não posso importar um save vazio!")
            return

        try:
            game_list = GameList(json.loads(json_obj)["games"])
            save_gamelist()
            await ctx.send(":pencil2: | Lista de jogos salva!")
        except:
            await ctx.send(":warning: | Esta lista de jogos é invalida")
        
        return

bot.run(getenv("BDG_TOKEN"))