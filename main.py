import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Everything is loaded up, bot is ready for use! \n\tPrefix is: "$" \n\tBot\' user tag is: \'{0.user}\''.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Zdravím, jsem Smrček a ty by jsi si měl koupit větší brýle!')

client.run('ODU1NDk2ODgwODYyMjY1NDE0.YMzVjg.SbuCfKwEn7roHxtMSy8j5B2ZvLE')
