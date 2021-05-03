import requests
import datetime
import os
import pytz
from decouple import config

def main():

	discord_url  = config('DISCORD_URL')

	josiah_access_token = config('ACCESS_TOKEN')
	kartik_access_token = config('KARTIK_ACCESS_TOKEN')
	final_str = ""
	final_str += get_leaderboard(josiah_access_token)
	final_str += get_daily_steps_leaderboard([josiah_access_token, kartik_access_token])

	print(final_str)


	data = {"content": final_str}
	response = requests.post(discord_url, json=data)



def get_leaderboard(access_token):
	header = {'Authorization': 'Bearer {}'.format(access_token)}
	response = requests.get("https://api.fitbit.com/1.1/user/-/leaderboard/friends.json", headers=header).json()


	id_hash = {}

	for person in response['included']:
	    id_hash[person['id']] = person['attributes']['name']

	date = get_current_date()


	final_str = "---------------------------------\n" + 'Fitbit Leaderboard ' + date.strftime("%x") + "\n---------------------------------\n"
	for data in response['data']:
		user_id = data['relationships']['user']['data']['id']
		rank = data['attributes']['step-rank'] 
		step_count = data['attributes']['step-summary'] 
		append_str = str(rank) + ". " + id_hash[user_id] + " - " + str(int(step_count))
		final_str += append_str + '\n'
	return final_str


def get_daily_steps_leaderboard(access_tokens):
	formatted_date = get_current_date().strftime('%Y-%m-%d')

	steps_hash = {}
	for access_token in access_tokens:
		header = {'Authorization': 'Bearer {}'.format(access_token)}
		response = requests.get("https://api.fitbit.com/1/user/-/activities/date/" + formatted_date + ".json", headers=header).json()
		steps_hash[get_daily_steps(response)] = get_full_name(access_token)

	final_str = "---------------------------------\n" + 'Daily Step Counts ' + "\n---------------------------------\n"
	i = 1
	for daily_step_count in sorted(steps_hash.keys(), reverse=True):
		append_str = str(i) + ". " + steps_hash[daily_step_count] + " - " + str(daily_step_count)
		final_str += append_str + '\n'
		i+=1
	return final_str



def get_daily_steps(response):
	return response['summary']['steps']


def get_current_date():
	date = datetime.datetime.now(tz=pytz.utc)
	return date.astimezone(pytz.timezone('US/Pacific'))

def get_full_name(access_token):
	header = {'Authorization': 'Bearer {}'.format(access_token)}
	response = requests.get("https://api.fitbit.com/1/user/-/profile.json", headers=header).json()
	return response['user']['displayName']

main()






	