from league_of_legends_api.Api.leaugue_api import SummonerV4, MatchV4
from league_of_legends_api.Database.database import Database

db = Database()
#db.save_keys_to_database(keys)
keys = db.load_keys_in()
summoner = SummonerV4(keys)
salty, key = summoner.get_summoner_by_name("SaItySurprise")
match = MatchV4(keys)
response = match.get_match_list_by_account_id(salty['accountId'], key.id, champion='1', season='11')

print(response)
