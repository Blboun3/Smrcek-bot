# SMRČEK BOT
# Autor: Blboun3
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
from googletrans import Translator
from time import sleep

# Nadefinování překladače
translator = Translator()
translator = Translator(service_urls=['translate.googleapis.com']) # Nastevní URL adresy, kterou googletrans bude používat
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
    # Různé pozdravy, mezi kterými si náhodně vybere
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
            elif random.randint(0,100) < 2: # 5% Easter EGG
                await message.channel.send("JAK TI CHUTNALA KYTKA K VEČEŘI ?")
            elif random.randint(0,100) < 2: # 7% Easter EGG
                await message.channel.send("MÁM VELKÝ BRÝLE!")
            elif random.randint(0,100) < 2: # 10% Easter EGG
                await message.channel.send("Čau <@!452547916184158218> !")
            else: # Pokud není easter egg
                text = random_page() # Vygeneruj náhodný článek z Wikipedie
                rando = random_translate(text, "cs") # Přeložení do náhodného jazyka

                for i in range(11): # Náhodně krát přelož
                    rando = random_translate(rando[0].text, rando[1]) # Přeložení do náhodného jazyka

                translated = translator.translate(rando[0].text, dest="cs", src=rando[1]) # Přeložení zpátky do češtiny

                await message.channel.send(translated.text) # Poslání náhodného článku


# ------------------------- BOT COMMANDS ------------------------


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

# Funkce na přeložení textu do náhodného jazyka
def random_translate(text, Vsrc):
    langs = ["ja", "la", "de", "be", "da", "fi", "fr", "el", "hu", "it", "lt", "pl", "pt", "ru", "ro", "sk" ,"tr"] # Seznam jazyků
    Vdest = random.choice(langs) # Vybrání náhodného jazyka z pole
    while Vsrc == Vdest: # Pokud jsou jazyky stejné
        Vdest = random.choice(langs) # Vyber nový jazyk
    # Přeložení textu
    translated = translator.translate(text, dest=Vdest, src=Vsrc)
    # Vrácení textu + jazyku v jakém je
    print("----------------------")
    print(text)
    print(translated)
    return [translated, Vdest]


load_dotenv() # Načtení .env souboru
bot.run(os.getenv("TOKEN")) # Spuštění bota
