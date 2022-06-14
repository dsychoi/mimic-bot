import discord
import os
import requests
import random
import pickle
import pandas as pd
import re
import string

# from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from replit import db
from cont import cont


client = discord.Client()


def transcribe(play_code):
    """ Web scrapes for Shakespeare plays """
    text = requests.get(f"https://www.folgerdigitaltexts.org/{play_code}/text").text
    replaced_text = text.replace('<br/>','')
    return replaced_text


def clean_data(text):
  """ Cleans the transcripts """
  text = text.lower()
  text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
  text = re.sub('\w*\d\w*', '', text)
  text = re.sub('[‘’“”…]', '', text)
  text = re.sub('\n', '', text)
  return text


def markov_chain(text):
  """ Markov Chain function that creates a dictionary """
  words = text.split(' ')
  m_dict = defaultdict(list)
  for current_word, next_word in zip(words[0:-1], words[1:]):
    m_dict[current_word].append(next_word)
  m_dict = dict(m_dict)
  return m_dict


def generate_sentence(chain, count = random.randint(5,20)):
  """ Random text generator with a dictionary input """
  word1 = random.choice(list(chain.keys()))
  sentence = word1.capitalize()
  for i in range(count - 1):
    word2 = random.choice(chain[word1])
    word1 = word2
    sentence += ' ' + word2
  punctuation = [".", "!", "?"]
  sentence += random.choice(punctuation)
  return sentence


def store_quote(quote):
  """ Stores a quote inside of the Replit database """
  if "quotes" in db.keys():
    quotes = db["quotes"]
    quotes.append(quote)
    db["quotes"] = quotes
  else:
    db["quotes"] = [quote]


def delete_quote(index):
  """ Deletes a quote from the Replit database at the specified index """
  quotes = db["quotes"]
  if len(quotes) > index:
    del quotes[index]
    db["quotes"] = quotes
    

play_codes = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham',
              '1H4', '2H4', 'H5', '1H6', '2H6', '3H6', 'H8', 'JC',
              'Jn', 'Lr', 'LLL', 'Mac', 'MM', 'MV', 'Wiv',
              'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3', 'Rom',
              'Shr', 'Tmp', 'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK', 'WT']


play_names = ["All's Well That Ends Well", "Antony and Cleopatra", "As You Like It",
              "The Comedy of Errors", "Coriolanus", "Cymbeline", "Hamlet", "Henry IV Part 1",
              "Henry IV Part 2", "Henry V", "Henry VI Part 1", "Henry VI Part 2", "Henry VI Part 3",
              "Henry VIII", "Julius Caesar", "King John", "King Lear", "Love's Labor's Lost",
              "Macbeth", "Measure for Measure", "The Merchant of Venice", "The Merry Wives of Windsor",
              "A Midsummer Night's Dream", "Much Ado About Nothing", "Othello", "Pericles", "Richard II",
              "Richard III", "Romeo and Juliet", "The Taming of the Shrew", "The Tempest", "Timon of Athens",
              "Titus Andronicus", "Troilus and Cressida", "Twelfth Night", "Two Gentlemen of Verona",
              "Two Noble Kinsmen", "The Winter's Tale"]

### Collecting all of the transcripts using the web scraping function
# plays = []
# for code in play_codes:
#     plays.append(transcribe(code))


# transcripts_dict = dict(zip(play_names, plays))


### Pickling the transcripts of all the plays into a separate directory called "plays"
# os.mkdir('plays')
# for i, c in enumerate(play_names):
#   with open("plays/" + c + ".txt", "wb") as file:
#     pickle.dump(plays[i], file)


# Unpickling the files and creating the dictionary
data = {}
for i, c in enumerate(play_names):
  with open("plays/" + c + ".txt", "rb") as file:
    data[c] = pickle.load(file)

    
# Using pandas to turn the data into a corpus
pd.set_option("max_colwidth", 150)
data_df = pd.DataFrame.from_dict(data, orient = 'index')
data_df.columns = ['transcript']
data_df = data_df.sort_index()


### Using sci-kit learn to create a document term matrix
# cleaning = lambda x: clean_data(x)
# data_clean = pd.DataFrame(data_df.transcript.apply(cleaning))
# cv = CountVectorizer(stop_words = 'english')
# data_cv = cv.fit_transform(data_clean.transcript)
# data_dtm = pd.DataFrame(data_cv.toarray(), columns = cv.get_feature_names())


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
    choose_name1 = random.choice(play_names)
    choose_name2 = data_df.transcript.loc[choose_name1]
    choose_dict = markov_chain(choose_name2)
    # Uses generate_sentence function to generate text alongside title of play
    await message.channel.send(f"```{generate_sentence(choose_dict)}\n- randomly generated text using the Shakespeare play: {choose_name1}```")

  
  if msg.startswith("!write"):
    quote = msg.split("!write ", 1)[1]
    store_quote(quote)
    await message.channel.send("New quote has been stored.")

  
  if msg.startswith("!erase"):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("!erase", 1)[1])
      delete_quote(index)
      quotes = db["quotes"]
    await message.channel.send(quotes)

  
  if msg.startswith("!read"):
    await message.channel.send(random.choice(db["quotes"]))

  
  if msg.startswith("!list"):
    quotes = []
    if "quotes" in db.keys():
      quotes = db["quotes"]
    list_quotes = []
    for quote in db["quotes"]:
      list_quotes.append(quote)
    for quote in list_quotes:
      await message.channel.send(quote)

  
  if msg.startswith("!wipe"):
    db["quotes"].clear()
    await message.channel.send("All quotes have been deleted.")

  
  if msg.startswith("!commands"):
    await message.channel.send("```\n!hello: Says hello\n!quote: Generates a random blurb using a random Shakespeare play\n!write Insert Message Here: Stores a quote of your choice\n!read: Reads out a random user inputted quote\n!erase [index position]: Erases a stored quote at the specified index position\n!list: Shows a list of all stored user inputted quotes \n!wipe: Erases all stored user inputted quotes```")

    
# Keeps the bot running using Flask and Uptime Robot
cont()
my_secret = os.environ['token']
client.run(my_secret)