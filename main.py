import discord
import os
import random
from dotenv import load_dotenv

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if random.randint(0,100) < 50:
        text = random_page()
        await message.channel.send(text)

    if message.content.startswith('🌲hello'):
        await message.channel.send('Zdravím, jsem Smrček a ty by jsi si měl koupit větší brýle!')

# když bot jde online
@client.event
async def on_ready():
    print("---------------------------------------")
	# Počítadlo serverů
    guild_count = 0
	# Projití všech guild, ve kterých bot je
    for guild in client.guilds:
		# napsání jména a id serveru
        print(f"{guild_count+1} - {guild.id} (name: {guild.name})")
		# zvýšení počítadla
        guild_count = guild_count + 1

	# Vypsání výsledků
    print("---------------------------------------")
    print('Everything is loaded up, bot is ready for use! \n\tPrefix is: "$" \n\tBot\' user tag is: \'{0.user}\''.format(client))
    print("\tSmrček bot is in  " + str(guild_count) + " guilds\n")

import wikipedia
wikipedia.set_lang('cs')

def random_page():
   random = wikipedia.random(1)
   try:
       result = wikipedia.page(random).summary
   except wikipedia.exceptions.DisambiguationError as e:
       result = random_page()
   return result

load_dotenv()
client.run(os.getenv("TOKEN"))
