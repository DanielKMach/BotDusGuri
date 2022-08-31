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

template = {
	"_id": "games",
	"games": []
}

class GameList:

	_games: list[dict[str, any]]
	_collection: pymongo.collection.Collection
	_document_id: str

	def __init__(self, mongo_collection: pymongo.collection.Collection):
		self.set_mongo(mongo_collection)
		self.load_from_mongo()

	@property
	def games(self):
		return self._games

	@property
	def collection(self):
		return self._collection

	def create_game(self, name: str, *, source: str = None, icon_url: str = None, added_by: int = None) -> int:
		game = {
			"name": name
		}
		if source != None and len(source) > 3:
			game["source"] = source

		if icon_url != None and len(icon_url) > 3:
			game["icon"] = icon_url

		if added_by != None:
			game["added_by"] = added_by

		self._games.append(game)

		return self.index_of(game['name'])

	def remove_game(self, index: int):
		del(self._games[index])

	def rate_game(self, index: int, author: int, rating: float, opinion: str = None):
		rating = max(min(rating, 10), 0)
		
		rating_obj = {
			"rating": rating,
			"author": author,
			"opinion": opinion
		}

		ratings = self._games[index].get("ratings", [])

		has_already_rated = self.get_rating(index, author)
		if has_already_rated == None:
			ratings.append(rating_obj)
		else:
			ratings[has_already_rated] = rating_obj

		self._games[index]["ratings"] = ratings


	# Get/Set information functions
	def get_name(self, index: int) -> str:
		return self._games[index]["name"]

	def set_name(self, index: int, name: str):
		self._games[index]["name"] = name;

	def get_rating(self, index: int, author: int) -> dict[str, any]:
		ratings = self._games[index].get("ratings", [])
		for i in range(len(ratings)):
			if ratings[i]["author"] == author:
				return i
		return None

	def get_ratings(self, index: int) -> list[dict[str, any]]:
		return self._games[index].get("ratings", [])

	def get_rating_median(self, index: int) -> float:
		ratings = self._games[index].get("ratings", [])
		if len(ratings) == 0:
			return None

		rating_sum = 0

		for rating in ratings:
			rating_sum += rating["rating"]

		return rating_sum / len(ratings)

	def has_been_rated(self, index: int) -> bool:
		return len(self.get_ratings(index)) > 0

	def get_added_by(self, index: int) -> int:
		return self._games[index].get("added_by", None)

	def get_source(self, index: int) -> str:
		return self._games[index].get("source", None)

	def set_source(self, index: int, source: str):
		self._games[index]["source"] = source

	def get_icon(self, index: int) -> str:
		return self._games[index].get("icon", None)

	def set_icon(self, index: int, icon_url: str):
		self._games[index]["icon"] = icon_url


	# Get index functions
	def index_of(self, game_name: str) -> int:
		for i in range(len(self._games)):
			if self._games[i]["name"].lower() == game_name.lower():
				return i

	def index_of_closest(self, game_name: str) -> int:
		results = difflib.get_close_matches(game_name, self.get_name_list())
		if len(results) <= 0:
			return None
		
		return self.index_of(results[0])


	def get_name_list(self) -> list[str]:
		game_names: list[str] = []
		for game in self._games:
			game_names.append(game["name"])

		return game_names

	def get_rating_median_list(self) -> list[float]:
		ratings_meds: list[float] = []
		for i in range(len(self._games)):
			ratings_meds.append(self.get_rating_median(i))

		return ratings_meds

	def has_user_rated_game(self, index: int, user_id: int) -> bool:
		game_ratings = self.get_ratings(index)
		for rating in game_ratings:
			if rating["author"] == user_id:
				return True
		return False

	def sort(self):
		self._games = sorted(self._games, key=lambda k: k['name'])

	def filter(self, filter: GameFilter):
		count = range(len(self.games))
		for i in count:
			if filterFunctions[filter.value](self, i):
				yield i

	# JSON related functions
	def from_json(self, json_obj: dict[str, any]):
		if type(json_obj.get("games", None)) == list:
			self._games = list(json_obj["games"])

		self.sort()

	def to_json(self) -> dict[str, any]:
		self.sort()

		return {
			"games": self._games
		}

	# MongoDB related functions
	def set_mongo(self, mongo_collection: pymongo.collection.Collection, document_id: str = "games"):
		self._collection = mongo_collection

	def save_to_mongo(self):
		print(f"Salvando gamelist para a coleção {self.collection.name}...")

		jsonobj = self.to_json()

		self.collection.update_one(
			{"_id": "games"},
			{"$set": jsonobj},
			upsert=True
		)

	def load_from_mongo(self):
		print("Carregando gamelist da coleção...")
		doc = self.collection.find_one({"_id": "games"})
		if doc == None:
			self.collection.insert_one(template)
			doc = dict(template)

		self.from_json(doc)