from database import Quote
from processing import Processor
from processing import data_df
from processing import play_names
import random
import discord
import os

from replit import db
from cont import cont


client = discord.Client()
quoter = Quote()
processor = Processor()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("!hello"):
    await message.channel.send("Hello!")

  if msg.startswith("!quote"):
    # Chooses a random Shakespeare play
    choose_play_name = random.choice(play_names)
    play_transcript = data_df.transcript.loc[choose_play_name]
    choose_dict = processor.markov_chain(play_transcript)
    # Uses generate_sentence function to generate text alongside title of play
    await message.channel.send(f"```{processor.generate_sentence(choose_dict)}\n- randomly generated text using the Shakespeare play: {choose_play_name}```")

  
  if msg.startswith("!write"):
    quote = msg.split("!write ", 1)[1]
    quoter.store_quote(quote)
    await message.channel.send("New quote has been stored.")

  elif msg.startswith("!erase"):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("!erase", 1)[1])
      quoter.delete_quote(index)
      quotes = db["quotes"]
    await message.channel.send(quotes)

  elif msg.startswith("!read"):
    await message.channel.send(random.choice(db["quotes"]))

  elif msg.startswith("!list"):
    quotes = []
    if "quotes" in db.keys():
      quotes = db["quotes"]
    list_quotes = []
    for quote in db["quotes"]:
      list_quotes.append(quote)
    for quote in list_quotes:
      await message.channel.send(quote)

  elif msg.startswith("!wipe"):
    db["quotes"].clear()
    await message.channel.send("All quotes have been deleted.")

  elif msg.startswith("!commands"):
    await message.channel.send('''```
 !hello - Greets the user
 !quote - Generates a random text blurb using one of Shakespeare's plays
 !write [text to save] - Saves text that will be randomly selected when using the !read command. Can be erased using !erase.
 !read - Randomly selects a text that was saved by !write and spits it out.
 !erase [index position] - Erases saved text at the specified index position.
 !list - Prints out a list of saved text in sequential order. Index position starts at 0.
 !wipe - Wipes all saved text.```''')

# Keeps the bot running using Flask and Uptime Robot
cont()
my_secret = os.environ['token']
client.run(my_secret)