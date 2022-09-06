from multiprocessing.sharedctypes import Value
import pymongo.collection
import difflib
import enum

__all__ = ["GameFilter", "GameList"]

class GameFilter(enum.Enum):
	ALL         = 0
	RATEDONLY   = 1
	UNRATEDONLY = 2
	ABOVE5      = 3
	BELOW5      = 4

filterFunctions = {
	lambda g, i: True,
	lambda g, i: g.has_been_rated(i),
	lambda g, i: not g.has_been_rated(i),
	lambda g, i: g.get_rating_median(i) > 5,
	lambda g, i: g.get_rating_median(i) <= 5,
}

class Game:
	def __init__(self):
		self._name: str = "Undefined"
		self._source: str = None
		self._icon: str = None
		self._added_by: int = None

		self._ratings: list[dict[str, any]] = []

	@property
	def name(self):
		return self._name

	@property
	def source(self):
		return self._source

	@property
	def icon(self):
		return self._icon

	@property
	def added_by(self):
		return self._added_by

	@property
	def ratings(self) -> list[dict[str, any]]:
		return self._ratings

	@property
	def rating_median(self) -> float | None:
		if len(self.ratings) == 0:
			return

		sum = 0
		for r in self.ratings:
			sum += r['rating']

		return sum / len(self.ratings)

	@property
	def has_been_rated(self) -> bool:
		return len(self.ratings > 1)

	def rate(self, *, author: int, rating: float, opinion: str = None):
		
		if not isinstance(author, int): raise TypeError("'author_id' must be an instance of type 'int'")
		if not isinstance(rating, float): raise TypeError("'rating' must be an instance of type 'float'")
		
		rating_obj = {
			'rating': max(min(rating, 10), 0), # clamp(rating, 0, 10)
			'author': author
		}
		if isinstance(opinion, str):
			rating_obj['opinion'] = opinion

		author_rating = self.get_user_rating(author)
		if author_rating != None:
			self.ratings[author_rating] = rating_obj
		else:
			self.ratings.append(rating_obj)

	def get_user_rating(self, author_id) -> int | None:
		for r in range(len(self.ratings)):
			rating = self.ratings[r]
			if rating.get('author') and rating['author'] == author_id:
				return r

	def from_dict(self, dic: dict[str, any], /):
		if not dic.get('name'): raise ValueError("'jsonobj' must have an attribute 'name'")
		if not isinstance(dic['name'], str): raise TypeError("'name' attribute must be an instance of type 'str'")

		self._name = dic['name']

		if isinstance(dic.get('source'), str):   self._source = dic['source']
		if isinstance(dic.get('icon'), str):     self._icon = dic['icon']
		if isinstance(dic.get('added_by'), int): self._added_by = dic['added_by']
		if isinstance(dic.get('ratings'), list): self._ratings = dic['ratings']

	def to_dict(self) -> dict[str, any]:
		dic = {}
		if self._name != None: dic['name'] = self._name
		if self._source != None: dic['source'] = self._source
		if self._icon != None: dic['icon'] = self._icon
		if self._added_by != None: dic['added_by'] = self._added_by
		if self._ratings != None: dic['ratings'] = self._ratings

		return dic


class GameList:

	def __init__(self, mongo_collection: pymongo.collection.Collection):
		self._games: list[Game] = None
		self._collection: pymongo.collection.Collection = None
		self._document_id: str = None

		self._collection = mongo_collection
		self.load_from_mongo()

	@property
	def games(self):
		return self._games

	@property
	def collection(self):
		return self._collection

	def __getitem__(self, i: int | str) -> Game | None:
		if isinstance(i, int):
			return self.games[i]

		elif isinstance(i, str):
			index = self.index_of_closest(i)
			if index == None: return
			return self[index]

		raise TypeError("'i' must be an instance of type 'int' or 'str'")

	def create_game(self, name: str, *, source: str = None, icon_url: str = None, added_by: int = None) -> Game:

		if not isinstance(name, str):
			raise TypeError("'name' must be an instance of type 'str'")
		
		game = Game()

		game.from_dict({
			'name': name,
			'source': source,
			'icon': icon_url,
			'added_by': added_by
		})

		self.games.append(game)
		return game

	def delete_game(self, i: int, /) -> Game:
		game = self.games[i]
		del(self.games[i])
		return game

	# Get index functions
	def index_of(self, game_name: str) -> int | None:
		game_name = game_name.lower()

		for i in range(len(self)):
			if self.games[i]._name.lower() == game_name:
				return i

	def index_of_closest(self, game_name: str) -> int | None:
		names = [ game.name for game in self.games ]
		results = difflib.get_close_matches(game_name, names)
		if len(results) > 0:
			return self.index_of(results[0])

	def sort(self):
		self._games = sorted(self.games, key=lambda k: k.name)

	def filter(self, filter: GameFilter):
		count = range(len(self.games))
		for i in count:
			if filterFunctions[filter.value](self, i):
				yield i

	# JSON related functions
	def from_dict(self, dic: dict[str, any], /):
		dgames = dic.get('games')
		if dgames == None: raise ValueError("'dic' must have an attribute 'games'")
		if not isinstance(dgames, list): raise TypeError("'games' attribute must be an instance of type 'list'")

		self._games = []
		for dgame in dgames:
			if isinstance(dgame, dict):
				game = Game()
				game.from_dict(dgame)
				self.games.append(game)

		self.sort()

	def to_dict(self) -> dict[str, any]:
		self.sort()

		return { 'games': [ game.to_dict() for game in self.games ] }

	def save_to_mongo(self):
		print(f"Salvando gamelist para a coleção '{self.collection.name}'...")

		dic = self.to_dict()

		self.collection.update_one(
			{"_id": "games"},
			{"$set": dic},
			upsert=True
		)

	def load_from_mongo(self):
		print(f"Carregando gamelist da coleção '{self.collection.name}'...")
		doc = self.collection.find_one({'_id': 'games'})
		if doc == None:
			doc = {'_id': 'games', 'games': []}

		self.from_dict(doc)

	def __len__(self) -> int:
		return len(self.games)