import asyncio
import bdg
import os

if __name__ == "__main__":
	bot = bdg.BotDusGuri()
	bot.load_config("bdg.config.json")
	bot.connect_to_mongo(os.getenv("MONGO_URI"))
	asyncio.run(bot.load_commands())
	asyncio.run(bot.load_triggers())
	bot.run(os.getenv("TOKEN"))