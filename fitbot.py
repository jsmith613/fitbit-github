import requests
import datetime
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

	date = get_current_date()


	webhook = Webhook.from_url(discord_url, adapter=RequestsWebhookAdapter())
	e = discord.Embed(
		title="Daily Fitbot " + date.strftime("%x"), 
		color=65520, 
		description="",
		thumbnail='https://logos-world.net/wp-content/uploads/2021/02/Fitbit-Emblem.png',
		url='https://www.fitbit.com/')
	e.add_field(name="__Fitbit Leaderboard__", value=get_leaderboard(josiah_access_token), inline=True)
	e.add_field(name="__Daily Step Counts__", value=get_daily_steps_leaderboard([josiah_access_token, kartik_access_token, sup_access_token, rishi_access_token]), inline=True)
	e.set_thumbnail(url='https://logos-world.net/wp-content/uploads/2021/02/Fitbit-Emblem.png')


	webhook.send(embed=e)



def get_leaderboard(access_token):
	header = {'Authorization': 'Bearer {}'.format(access_token)}
	response = requests.get("https://api.fitbit.com/1.1/user/-/leaderboard/friends.json", headers=header).json()


	id_hash = {}

	for person in response['included']:
	    id_hash[person['id']] = person['attributes']['name']

	date = get_current_date()


	final_str = '\n'
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

	final_str = '\n'
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






	