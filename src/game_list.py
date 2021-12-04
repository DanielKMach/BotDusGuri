from discord_slash.utils.manage_commands import create_choice

class GameList:

    _games: list

    def __init__(self, games=[]):
        self._games = games


    def create_game(self, name, source=None, added_by=None):
        game = {
            "name": name
        }
        if source != None:
            game["source"] = source

        if added_by != None:
            game["added_by"] = added_by

        self._games.append(game)

    def remove_game(self, index):
        del(self._games[index])

    def sort(self):
        self._games = sorted(self._games, key=lambda k: k['name'])

    def rate_game(self, index, author, rating, opinion=None):
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

    def get_name(self, index):
        return self._games[index]["name"]

    def set_name(self, index, name):
        self._games[index]["name"] = name;

    def get_rating(self, index, author):
        ratings = self._games[index].get("ratings", [])
        for i in range(len(ratings)):
            if ratings[i]["author"] == author:
                return i
        return None

    def get_rating_median(self, index):
        ratings = self._games[index].get("ratings", [])
        if len(ratings) == 0:
            return None

        rating_sum = 0

        for rating in ratings:
            rating_sum += rating["rating"]

        return rating_sum / len(ratings)

    def get_ratings(self, index):
        return self._games[index].get("ratings", [])

    def has_been_rated(self, index):
        return len(self.get_ratings(index)) > 0

    def get_source(self, index):
        return self._games[index].get("source", None)

    def get_added_by(self, index):
        return self._games[index].get("added_by", None)

    def set_source(self, index, source):
        self._games[index]["source"] = source

    def get_icon(self, index):
        return self._games[index].get("icon", None)

    def set_icon(self, index, icon_source):
        self._games[index]["icon"] = icon_source

    def index_of(self, game_name):
        for i in range(len(self._games)):
            if self._games[i]["name"].lower() == game_name.lower():
                return i


    def get_name_list(self):
        game_names = []
        for game in self._games:
            game_names.append(game["name"])

        return game_names

    def get_rating_median_list(self):
        ratings_meds = []
        for i in range(len(self._games)):
            ratings_meds.append(self.get_rating_median(i))

        return ratings_meds

    def has_user_rated_game(self, index, user_id):
        game_ratings = self.get_ratings(index)
        for rating in game_ratings:
            if rating["author"] == user_id:
                return True
        return False

    def get_choices(self):
        choices = []
        
        for i in range(len(self._games)):
            choices.append(
                create_choice(
                    name=self._games[i]["name"],
                    value=self._games[i]["name"],
                )
            )

        if len(self._games) < 1:
            choices.append(
                create_choice(
                    name="Inválido",
                    value="Invalid",
                )
            )
        
        return choices

    def to_string(self):
        return str(self._games)

    
    def load_json(self, json_obj={}):
        if type(json_obj.get("games", None)) == list:
            self._games = json_obj["games"]

    def get_json(self):
        return {"_name": "games", "games": self._games}

    def set_mongo_collection(self, mongo_collection, search_filter={"_name": "games"}):
        self._mongo_collection = mongo_collection
        self._search_filter = search_filter

    def save_to_mongo(self):
        print("Saving gamelist to collection...")
        self._mongo_collection.update_one(
            self._search_filter,
            {'$set': {"games": self._games}},
            upsert=True
        )

    def load_from_mongo(self):
        print("Loading gamelist from collection...")
        doc = self._mongo_collection.find_one(self._search_filter)
        if doc != None:
            self.load_json(doc)



def build_gamelist(mongo_collection):
    gamelist = GameList()
    gamelist.set_mongo_collection(mongo_collection)
    gamelist.load_from_mongo()

    return gamelist