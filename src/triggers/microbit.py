from serial import Serial

class MicrobitMessageTrigger:

    def __init__(self, e):

        try:
            serial = Serial(port="COM4", baudrate=115200, timeout=0.5)
            if not serial.is_open:
                serial.Open()
        except Exception as error:
            print("Não foi possível estabelecer conexão com Serial:\n"+str(error))
            return

        @e.bot.event
        async def on_message(message):
            if message.channel.id == 922595210888904705:
                print("Serial sent")
                serial.write(str.encode(message.content))

        #@e.bot.event
        #async def on_ready():
        #    channel = e.bot.get_channel(922595210888904705)
        #    while True:
        #        