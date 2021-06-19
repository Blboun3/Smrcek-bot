# Import knihoven
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import os
import random
from dotenv import load_dotenv
import wikipedia
import nacl
from gtts import gTTS
from time import sleep

# Nastavení jazyku wikipedia na češtinu
wikipedia.set_lang('cs')
# Bot object
bot = commands.Bot(command_prefix="🌲",description="Smrček bot, všichni známe Smrčka...")

"""
----------------   BOT EVENTY   ----------------
"""
stillPlaying = True
# když bot jde online
@bot.event
async def on_ready():
    print("---------------------------------------")
	# Počítadlo serverů
    guild_count = 0
	# Projití všech guild, ve kterých bot je
    for guild in bot.guilds:
		# napsání jména a id serveru
        print(f"{guild_count+1} - {guild.id} (name: {guild.name})")
		# zvýšení počítadla
        guild_count = guild_count + 1

	# Vypsání výsledků
    print("---------------------------------------")
    print('Everything is loaded up, bot is ready for use! \n\tPrefix is: "🌲" \n\tBot\' user tag is: \'{0.user}\''.format(bot))
    print("\tSmrček bot is in  " + str(guild_count) + " guilds")
    print("---------------------------------------")

# Když zpráva:
@bot.event
async def on_message(message):
    if message.author == bot.user: # Pokud ji napsal bot, tak nic nedělej
        return
    if ("🌲" in message.content): # Pokud zpráva obsahuje prefix
        await bot.process_commands(message) # Spuštení command handleru
    else: # Pokud se nejedná o command
        # 10% šance, že napíše
        if random.randint(0,100) < 10:
            if random.randint(0,100) < 2: # 2% Easter EGG
                await message.channel.send("KUP SI VĚTŠÍ BRÝLE!")
            elif random.randint(0,100) < 5: # 5% Easter EGG
                await message.channel.send("JAK TI CHUTNALA KYTKA K VEČEŘI ?")
            elif random.randint(0,100) < 7: # 7% Easter EGG
                await message.channel.send("MÁM VELKÝ BRÝLE!")
            elif random.randint(0,100) < 10: # 10% Easter EGG
                await message.channel.send("Čau <@!452547916184158218> !")
            else: # Pokud není easter egg
                text = random_page() # Vygeneruj náhodný článek z Wikipedie
                await message.channel.send(text) # Poslání náhodného článku

"""
----------------   BOT COMMANDY   ----------------
"""

ffmpeg_options = {
    #'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


@bot.command(name="die", description="Odpojí smrčka z voicu")
async def die(ctx):
    pass

# Připojení do voicu
@bot.command(name="join", description="Připojí se do voice channelu a začne všechny poučovat....")
async def join(ctx,*, channel: discord.VoiceChannel):
        """Připojí se do voice channelu a začne všechny poučovat...."""
        try:
            #channel = discord.VoiceChannel
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)

            vc = await channel.connect() # Připojení do voicu

            play_file(vc) # Funkce, která hraje wikipedii

        except Exception as e:
            await ctx.send(e) # Napsání erroru

# Funkce na zpracování hudby
def play_file(vc):
    sleep(random.randint(0,15)) # Počkání 0 - 60 vteřin
    file = "file.mp3" # Jméno souboru
    txt = random_page() # Vygenerování náhodného souboru
    print(txt)
    # initialize tts, create mp3 and play
    tts = gTTS(txt, 'cz', lang="cs") # Vytvoření MP3
    tts.save(file) # Uložení MP3
    vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=file, **ffmpeg_options), after=lambda v: play_file(vc)) # Zahrání a následné znovu zavolání funkce

# Hello příkaz, sort of easter egg
@bot.command(name="hello",description="Pozdraví tak, jak by Smrček pozdravit měl")
async def hello(ctx):
    """Pozdraví tak, jak by Smrček pozdravit měl"""
    # Různé pozdravy, mezi kterými si náhodně vybere
    if random.randint(0,100) < 25:
        await ctx.send("Zdarec já sem Smrček! \nKUP SI VĚTŠÍ BRÝLE!")
    elif random.randint(0,100) < 25:
        await ctx.send("Já Smrček ty být: JAK TI CHUTNALA KYTKA K VEČEŘI ?")
    elif random.randint(0,100) < 25:
        await ctx.send("Já, Smrčkoslav Jedlička MÁM VELKÝ BRÝLE!")
    elif random.randint(0,100) < 15:
        await ctx.send("Smrček zdraví Čubíka! Čau <@!452547916184158218> !")
    elif random.randint(0,100) < 10:
        await ctx.send('Zdravím, jsem Smrček a ty by jsi si měl koupit větší brýle!')
    else:
        await ctx.send("BAF!")

# Funkce na získání náhodného wiki článku
def random_page():
   random = wikipedia.random(1)
   try:
       result = wikipedia.page(random).summary
   except wikipedia.exceptions.DisambiguationError as e:
       result = random_page()
   return result

load_dotenv() # Načtení .env souboru
bot.run(os.getenv("TOKEN")) # Spuštění bota
