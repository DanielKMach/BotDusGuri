from discord_slash.utils.manage_commands import create_choice

class GameList:

    _games: list

    def __init__(self, games=[]):
        self._games = games


    def create_game(self, name="Random Game", source=None):
        self._games.append({
            "name": name,
            "source": source
        })

    def remove_game(self, index):
        _games.remove_at(index)

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

    def get_source(self, index):
        return self._games[index].get("source", None)

    def set_source(self, index, source):
        self._games[index]["source"] = source

    def get_icon(self, index):
        return self._games[index].get("icon", "")

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

    def get_choices(self):
        choices = []
        
        for i in range(len(self._games)):
            choices.append(
                create_choice(
                    name=self._games[i]["name"],
                    value=self._games[i]["name"],
                )
            )
        
        return choices

    def to_string(self):
        return str(self._games)