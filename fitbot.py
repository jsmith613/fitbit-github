import requests
import datetime
from datetime import timedelta
import os
import pytz
from decouple import config
import discord
from discord import Webhook, RequestsWebhookAdapter

def main():

	discord_url  = config('DISCORD_URL')

	josiah_access_token = config('ACCESS_TOKEN')
	kartik_access_token = config('KARTIK_ACCESS_TOKEN')
	# ejnar_access_token = config('EJNAR_ACCESS_TOKEN')
	sup_access_token = config('SUP_ACCESS_TOKEN')
	rishi_access_token = config('RISHI_ACCESS_TOKEN')

	access_tokens = [josiah_access_token, kartik_access_token, sup_access_token, rishi_access_token]


	yesterday = get_current_date() - timedelta(days = 1)
	formatted_date = yesterday.strftime('%Y-%m-%d')

	webhook = Webhook.from_url(discord_url, adapter=RequestsWebhookAdapter())
	e = discord.Embed(
		title="Daily Fitbot " + yesterday.strftime("%x"), 
		color=65520, 
		description="",
		thumbnail='https://logos-world.net/wp-content/uploads/2021/02/Fitbit-Emblem.png',
		url='https://www.fitbit.com/')

	weekly_names_value, weekly_steps_value = get_leaderboard(josiah_access_token)
	e.add_field(name="__Weekly Steps__", value=weekly_names_value, inline=True)
	e.add_field(name='\u200b', value='\u200b', inline=True) # strictly for formatting
	e.add_field(name='⠀', value=weekly_steps_value, inline=True)

	

	daily_names_value, daily_steps_value = get_daily_steps_leaderboard(access_tokens, formatted_date)
	e.add_field(name="__Yesterday's Steps__", value=daily_names_value, inline=True)
	e.add_field(name='\u200b', value='\u200b', inline=True) # strictly for formatting
	e.add_field(name='⠀', value=daily_steps_value, inline=True)


	e.set_thumbnail(url='https://logos-world.net/wp-content/uploads/2021/02/Fitbit-Emblem.png')


	webhook.send(embed=e)

def get_leaderboard(access_token):
	header = {'Authorization': 'Bearer {}'.format(access_token)}
	response = requests.get("https://api.fitbit.com/1.1/user/-/leaderboard/friends.json", headers=header).json()


	id_hash = {}

	for person in response['included']:
	    id_hash[person['id']] = person['attributes']['name']


	names_str = '\n'
	steps_str = '\n'
	for data in response['data']:
		user_id = data['relationships']['user']['data']['id']
		rank = data['attributes']['step-rank'] 
		step_count = data['attributes']['step-summary'] 

		names_str += str(rank) + ". " + id_hash[user_id].replace('.', '') + ":"
		names_str += '\n'
		steps_str += f'{int(step_count):,}'
		steps_str += '\n'

	return names_str, steps_str

# date must be in YYYY-MM-DD format
def get_daily_steps_leaderboard(access_tokens, date):
	# hash from number of steps to name
	steps_hash = {}
	for access_token in access_tokens:
		header = {'Authorization': 'Bearer {}'.format(access_token)}
		response = requests.get("https://api.fitbit.com/1/user/-/activities/date/" + date + ".json", headers=header).json()
		steps_hash[get_daily_steps(response)] = get_full_name(access_token)

	names_str = '\n'
	steps_str = '\n'
	i = 1

	# sort hash by key (step number) 
	for daily_step_count in sorted(steps_hash.keys(), reverse=True):
		names_str += str(i) + ". " + steps_hash[daily_step_count].replace('.', '') + ":"
		names_str += '\n'
		steps_str += f'{daily_step_count:,}'
		steps_str += '\n'
		i+=1
	return names_str, steps_str


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






	