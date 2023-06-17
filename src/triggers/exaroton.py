import asyncio
import requests
import discord
import discord.ext.commands
import bdg
import websockets.client
import json

class ExarotonCog(discord.ext.commands.Cog, name="exaroton"):

	def __init__(self, bot: bdg.BotDusGuri):
		self.bot = bot
		self.sockets: list[Exaroton] = []

	async def on_start(self):

		for guild in self.bot.guilds:
			collection = self.bot.guild_collection(guild)
			document = collection.find_one({'_id': 'exaroton'})
			if document == None or not document.get('active', True):
				continue

			try:
				exaroton = Exaroton(self.bot, server=document['server'], token=document['token'], events=document.get('events', []))
				self.sockets.append(exaroton)
			except Exception as e:
				print(f"\033[91mNão foi possível carregar o exaroton de '{guild.name}' ({guild.id}): {e}\033[0m",)
				continue

			print(f"Conexão ao exaroton '{exaroton.name}' pronta")

		for exaroton in self.sockets:
			try:
				self.bot.loop.create_task(exaroton.start())
			except Exception as e:
				print(f"\033[91mNão foi possível iniciar o exaroton '{exaroton.name}': {e}\033[0m")	
				continue

			print(f"Conexão ao exaroton '{exaroton.name}' iniciada")

class Exaroton:

	@property
	def name(self) -> str:
		return self._info.get('name')
	
	@property
	def address(self) -> str:
		return self._info.get('address')
	
	@property
	def port(self) -> str | None:
		return self._info.get('port')
	
	@property
	def url(self) -> str:
		return self._url
	
	@property
	def websocket_url(self) -> str:
		return self._url.replace('https', 'wss') + "/websocket"
	
	@property
	def url_headers(self) -> str:
		return self._headers
	

	def __init__(self, bot: bdg.BotDusGuri, *, server: str, token: str, events: list):
		self.bot = bot
		self.players = set()

		self.token = token
		self.server = server

		self._url = f"https://api.exaroton.com/v1/servers/{self.server}"
		self._headers = { "authorization": f"Bearer {self.token}" }

		self.load_events(events)

		response = requests.get(self.url, headers=self.url_headers)

		if response.status_code != 200:
			raise ConnectionError(f"Não foi possível se conectar com o servidor, código: {response.status_code}")
		
		data = json.loads(response.text)['data']

		self._info = {
			'name': data['name'],
			'address': data['address'],
			'port': data['port']
		}

	def load_events(self, events: list):
		self.events = {}

		for event in events:
			event_type = event.get('event', None)
			channel = self.bot.get_channel(int(event.get('notification_channel', 0)))
			message = event.get('message', None)

			if event_type is None or channel is None or message is None:
				continue
			
			nodes = self.events.get(event_type, [])
			nodes.append({ 'channel': channel, 'message': message })
			self.events[event_type] = nodes

		self.event_names = self.events.keys()

	async def start(self):
		reconnection_attempts = 0

		while reconnection_attempts < 5:
			try:
				async with websockets.client.connect(self.websocket_url, extra_headers=self.url_headers) as websocket:

					if reconnection_attempts > 0:
						reconnection_attempts = 0
						print(f"Conexão à '{self.name}' reaberta com exito")

					async for data in websocket:
						await self._on_message(data)

			except websockets.ConnectionClosed:
				print(f"Conexão à '{self.name}' fachada. Tentando reconexão...")
				reconnection_attempts += 1
				await asyncio.sleep(5)

		print(f"\033[91mFalha ao reconectar à '{self.name}'\033[0m")

	async def _on_message(self, message):
		content = json.loads(message)

		if content['type'] == "status":
			players = set(content.get('data', {}).get('players', {}).get('list', self.players))
			
			if len(players) > len(self.players) and 'ON_PLAYER_JOIN' in self.event_names:
				player = tuple(players - self.players)[0]
				await self._on_player_join(player)

			if len(players) < len(self.players) and 'ON_PLAYER_LEAVE' in self.event_names:
				player = tuple(players - self.players)[0]
				await self._on_player_leave(player)

			self.players = players

	async def _on_player_join(self, player: str):
		for node in self.events['ON_PLAYER_JOIN']:
			message: str = node['message'].replace("&player", player)
			await node['channel'].send(message)

	async def _on_player_leave(self, player: str):
		for node in self.events['ON_PLAYER_LEAVE']:
			message: str = node['message'].replace("&player", player)
			await node['channel'].send(message)