import pandas as pd
import pickle
import random
import requests
import re
import string

import os

# from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict


class Processor:
  def transcribe(self, play_code):
      """ Web scrapes for Shakespeare plays """
      text = requests.get(f"https://www.folgerdigitaltexts.org/{play_code}/text").text
      replaced_text = text.replace('<br/>','')
      return replaced_text
  
  
  def clean_data(self, text):
    """ Cleans the transcripts """
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text
  
  
  def markov_chain(self, text):
    """ Markov Chain function that creates a dictionary """
    words = text.split(' ')
    m_dict = defaultdict(list)
    for current_word, next_word in zip(words[0:-1], words[1:]):
      m_dict[current_word].append(next_word)
    m_dict = dict(m_dict)
    return m_dict
  
  
  def generate_sentence(self, chain, count = random.randint(5,20)):
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

# Collecting all of the transcripts using the web scraping function
processor = Processor()
plays = []
for code in play_codes:
    plays.append(processor.transcribe(code))


transcripts_dict = dict(zip(play_names, plays))

# Pickling the transcripts of all the plays into a separate directory called "plays"
os.mkdir('plays')
for i, c in enumerate(play_names):
  with open("plays/" + c + ".txt", "wb") as file:
    pickle.dump(plays[i], file)

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

### Using sci-kit learn to create a document term matrix for future use
# cleaning = lambda x: clean_data(x)
# data_clean = pd.DataFrame(data_df.transcript.apply(cleaning))
# cv = CountVectorizer(stop_words = 'english')
# data_cv = cv.fit_transform(data_clean.transcript)
# data_dtm = pd.DataFrame(data_cv.toarray(), columns = cv.get_feature_names())