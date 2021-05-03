import requests
import datetime
import os
import pytz
from decouple import config

access_token = config('ACCESS_TOKEN')
discord_url  = config('DISCORD_URL')


header = {'Authorization': 'Bearer {}'.format(access_token)}
response = requests.get("https://api.fitbit.com/1.1/user/-/leaderboard/friends.json", headers=header).json()


id_hash = {}

for person in response['included']:
    id_hash[person['id']] = person['attributes']['name']

date = datetime.datetime.now(tz=pytz.utc)
date = date.astimezone(pytz.timezone('US/Pacific'))

final_str = "---------------------------------\n" + 'Fitbit Leaderboard ' + date.strftime("%x") + "\n---------------------------------\n"
for data in response['data']:
	user_id = data['relationships']['user']['data']['id']
	rank = data['attributes']['step-rank'] 
	step_count = data['attributes']['step-summary'] 
	append_str = str(rank) + ". " + id_hash[user_id] + " - " + str(int(step_count))
	final_str += append_str + '\n'
print(final_str)

data = {"content": final_str}
response = requests.post(discord_url, json=data)
	