from league_of_legends_api.Api.leaugue_api import SummonerV4
from league_of_legends_api.Database.database import Database

db = Database()
#db.save_keys_to_database(keys)
keys = db.load_keys_in()
summoner = SummonerV4(keys)
response = summoner.get_summoner_by_name("SaItySurprise")
print(response)
