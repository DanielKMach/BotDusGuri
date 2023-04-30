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

class Review:

	_author: int   = 0
	_rating: float = 0
	_opinion: str | None = None
	
	@property
	def author(self) -> int:
		return self._author
	
	@author.setter
	def author(self, value: int):
		self._author = value
	
	@property
	def rating(self) -> float:
		return self._rating
	
	@rating.setter
	def rating(self, value: float):
		self._rating = min(max(round(value, 1), 0), 10)
	
	@property
	def opinion(self) -> str | None:
		return self._opinion
	
	@opinion.setter
	def opinion(self, value: str | None):
		self._opinion = value


	def __init__(self, **kwargs):
		self.set(**kwargs)

	def set(self, **kwargs):
		if isinstance(a := kwargs.get('author'), (str, int)):   self.author  = int(a)
		if isinstance(b := kwargs.get('rating'), (float, int)): self.rating  = b
		if isinstance(c := kwargs.get('opinion'), str):         self.opinion = c

	def get(self) -> dict:
		return {
			'author':  str(self.author),
			'rating':  self.rating,
			'opinion': self.opinion
		}

class Game:

	_name: str          = "Undefined"
	_source: str | None = None
	_icon: str | None   = None
	_added_by: int      = 0
	_reviews: list[Review] = []

	@property
	def name(self) -> str:
		return self._name

	@property
	def source(self) -> str | None:
		return self._source

	@property
	def icon(self) -> str | None:
		return self._icon

	@property
	def added_by(self) -> int:
		return self._added_by

	@property
	def reviews(self) -> list[Review]:
		return self._reviews

	@property
	def rating_median(self) -> float | None:
		if not self.has_been_rated:
			return

		sum = 0
		for rating in self.reviews:
			sum += rating.rating

		return sum / len(self.reviews)

	@property
	def has_been_rated(self) -> bool:
		return len(self.reviews) > 0


	def __init__(self, **kwargs):
		self.set(**kwargs)

	def review(self, *, author: int, rating: float, opinion: str = None):
		review = Review(
			author = author,
			rating = rating,
			opinion = opinion
		)

		overwrite_review_index = self.index_of_user_rating(author)

		if overwrite_review_index != None:
			self.reviews[overwrite_review_index] = review
		else:
			self.reviews.append(review)


	def index_of_user_rating(self, author_id: int) -> int | None:
		for i in range(len(self.reviews)):
			rating = self.reviews[i]
			if rating.author == author_id:
				return i

	def set(self, **kwargs):
		if isinstance(a := kwargs.get('name'), str):            self._name = a
		if isinstance(b := kwargs.get('source'), str):          self._source = b
		if isinstance(c := kwargs.get('icon'), str):            self._icon = c
		if isinstance(d := kwargs.get('added_by'), (str, int)): self._added_by = int(d)
		if isinstance(e := kwargs.get('reviews'), list):        self._reviews  = list(Review(**rate) for rate in e)

	def get(self) -> dict:
		return {
			'name':     self.name,
			'added_by': str(self.added_by),
			'reviews':  list(rate.get() for rate in self.reviews),
			'icon':     self.icon,
			'source':   self.source
		}

class GameList:

	_games: list[Game] = []
	_collection: pymongo.collection.Collection | None = None

	@property
	def games(self) -> list[Game]:
		return self._games

	@property
	def collection(self) -> pymongo.collection.Collection | None:
		return self._collection
	

	def __init__(self, mongo_collection: pymongo.collection.Collection):
		self._collection = mongo_collection
		self.load_from_mongo()

	def __getitem__(self, i: int | str) -> Game | None:
		if isinstance(i, int):
			return self.games[i]

		elif isinstance(i, str):
			index = self.index_of_closest(i)
			if index == None: return
			return self[index]

		raise TypeError("'i' must be an instance of type 'int' or 'str'")

	def __len__(self) -> int:
		return len(self.games)
	

	def create_game(self, name: str, *, source: str = None, icon_url: str = None, added_by: int = None) -> Game:

		if not isinstance(name, str):
			raise TypeError("'name' must be an instance of type 'str'")
		
		game = Game(
			name=name,
			source=source,
			icon=icon_url,
			added_by=added_by
		)

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
	def load(self, dic: dict[str, any], /):
		games = dic.get('games')
		if games == None: raise ValueError("'dic' must have an attribute 'games'")
		if not isinstance(games, list): raise TypeError("'games' attribute must be an instance of type 'list'")

		self._games = []
		for game in games:
			if isinstance(game, dict):
				self.games.append(Game(**game))

		self.sort()

	def save(self) -> dict[str, any]:
		self.sort()

		return { 'games': [ game.get() for game in self.games ] }

	def save_to_mongo(self):
		print(f"Salvando gamelist para a coleção '{self.collection.name}'...")

		dic = self.save()

		print(dic)

		self.collection.update_one(
			{'_id': 'games'},
			{'$set': dic},
			upsert=True
		)

	def load_from_mongo(self):
		print(f"Carregando gamelist da coleção '{self.collection.name}'...")
		doc = self.collection.find_one({'_id': 'games'})
		if doc == None:
			doc = {'_id': 'games', 'games': []}

		self.load(doc)