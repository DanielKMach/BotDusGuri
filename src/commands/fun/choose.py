from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from random import randint

class ChooseCommand:

    def __init__(self, e):

        @e.slash.slash(
            name="escolher",
            description="Escolha entre 2 ou mais opções",
            options=[
                create_option(
                    name="escolhas",
                    description="As palavras para escolher, separado por espaços",
                    option_type=3,
                    required=True
                ),
            ],
            guild_ids=e.allowed_guilds
        )
        async def escolher(ctx, escolhas):

            choices = escolhas.split(" ")
            to_exit = False
            to_answer = True

            while not to_exit:
                chosen = choices[randint(0, len(choices) - 1)]

                if len(choices) > 1:
                    buttons = [
                        create_button(
                            style=ButtonStyle.blue,
                            label="Repetir",
                            custom_id="00"
                        ),
                        create_button(
                            style=ButtonStyle.green,
                            label=f"Repetir sem '{chosen}'",
                            custom_id="01"
                        ),
                        create_button(
                            style=ButtonStyle.red,
                            label="Não repetir",
                            custom_id="02"
                        )
                    ]

                    action_row = create_actionrow(*buttons)

                answer = ""
                if not to_answer and len(choices) > 1:
                    answer = f"\n*{len(choices) - 1} restantes*"

                if to_answer:
                    msg = await ctx.send(f":slot_machine: | O escolhido foi... **{chosen}**!"+answer, components=[action_row] if len(choices) > 1 else [])
                else:
                    msg = await ctx.channel.send(f":slot_machine: | O escolhido foi... **{chosen}**!"+answer, components=[action_row] if len(choices) > 1 else [])


                if len(choices) > 1:
                    button_ctx: ComponentContext = await wait_for_component(e.bot, components=action_row)
                    if button_ctx.custom_id == "00":
                        await msg.edit(components=[])
                        to_answer = False

                    if button_ctx.custom_id == "01":
                        await msg.edit(components=[])
                        to_answer = False
                        choices.remove(chosen)
                        if len(choices) <= 0:
                            await ctx.channel.send(":warning: | Não há mais itens na lista!")
                            to_exit = True

                    else:
                        await msg.edit(components=[])
                        to_exit = True

                else:
                    to_exit = True