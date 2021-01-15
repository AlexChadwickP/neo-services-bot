import os

import discord
from dotenv import load_dotenv
import pymongo

client = pymongo.MongoClient("mongodb+srv://root:n00dles2003@bugtracker.kcina.mongodb.net/Neocommissions?retryWrites=true&w=majority")
db = client["NeoCommissions"]
freelance_connection = db["Freelancer"]
commission_connection = db["Commission"]

load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

client = discord.Client()

ROLE_IDS = {
	'Bot Developer': '797874687861456977',
	'Spigot Developer': '797874722037170176',
	'Web Developer': '797900399616458792',
	'UI/UX Designer': '798230277553520671',
	'Software Developer': '798282315489869834'
}

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if message.content.startswith("$add-freelancer"):
		temp_command = message.content.replace("$add-freelancer", "")
		args = temp_command.split('&')
		final_args = []
		for argument in args:
			argument = argument.lstrip()
			final_args.append(argument)
		
		freelance_connection.insert_one({
			"name": final_args[0],
			"portfolio": final_args[1],
			"roles": final_args[2]
		})

		await message.channel.send(
			'Freelancer: ' + final_args[0] +
			'\nPortfolio: ' + final_args[1]
		)

	if message.content.startswith("$set-freelancer-portfolio"):
		temp_command = message.content.replace("$set-freelancer-portfolio", "")
		args = temp_command.split('&')
		final_args = []

		for argument in args:
			argument = argument.lstrip()
			final_args.append(argument)

		freelance_connection.update_one({ "name": final_args[0] }, { "$set": { "portfolio": final_args[1] } })

		await message.channel.send('Freelancer portfolio updated!')

	if message.content.startswith("$add-commission"):
		temp_command = message.content.replace("$add-commission", "")
		args = temp_command.split('&')
		final_args = []

		for argument in args:
			argument = argument.lstrip()
			final_args.append(argument)

		commission_connection.insert_one({
			"title": final_args[0],
			"description": final_args[1],
			"contact": final_args[2],
			"roles": final_args[3],
			"freelancer": "To be taken"
		})

		await message.channel.send("Commission inserted successfully")

	if message.content.startswith("$accept-commission"):
		temp_command = message.content.replace("$accept-commission", "")
		args = temp_command.split('&')
		final_args = []

		for argument in args:
			argument = argument.lstrip()
			final_args.append(argument)

	if message.content.startswith("$get-portfolio"):
		temp_command = message.content.replace("$get-portfolio", "")
		args = temp_command.split('&')
		final_args = []

		for argument in args:
			argument = argument.lstrip()
			final_args.append(argument)

		freelancer = freelance_connection.find_one({"name": final_args[0]})
		await message.channel.send("Portfolio is: " + freelancer["portfolio"])

	if message.content.startswith("$get-commissions"):
		for commission in commission_connection.find({ "freelancer": "To be taken" }):
			await message.channel.send(f"ID: {commission['_id']}\nTitle: {commission['title']}\nDescription: {commission['description']}\nType: <@&797577111212523531>")

	if message.content.startswith("$new-ticket"):
		guild = message.guild
		member = message.author
		admin_role = discord.utils.get(guild.roles, name="Administrator")
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True),
			admin_role: discord.PermissionOverwrite(read_messages=True)
		}
		channel = await guild.create_text_channel(f'{member}-ticket', overwrites=overwrites)

		await channel.send(f'Welcome to your ticket <@{member.id}>. Please tell us what you need, a timeline and your budget, unless you are looking for quotes, in which case it is not necessary to include the budget!')

	if message.content.startswith("$new-hr"):
		guild = message.guild
		member = message.author
		admin_role = discord.utils.get(guild.roles, name="Administrator")
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True),
			admin_role: discord.PermissionOverwrite(read_messages=True)
		}
		channel = await guild.create_text_channel(f'{member}-hr', overwrites=overwrites)

		await channel.send(f'Welcome to your hr ticket <@{member.id}>. Please let us know what you need help with!')

	if message.content.startswith("$help"):
		await message.channel.send('''
			$add-freelancer [DISCORD], [PORTFOLIO (if various links please use ";" between them)], [ROLES (if various roles please use ";" between them)]
			$set-freelancer-portfolio [PORTFOLIO (if various links please use ";" between them)]
			$help
		''')

client.run(TOKEN)