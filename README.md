# mimic-bot
A Natural Language Processing (NLP) Discord Bot

Primarily created for the purpose of using Shakespeare plays to generate text with Markov chains.


Using the [Folger Shakespeare API](https://shakespeare.folger.edu/the-folger-shakespeare-api/) to collect Shakespeare's complete works. 

Other usages: Interactivity with the Replit database in order to store user inputted quotes and return them at random.

# Deployment

Mimic Bot is hosted on the Replit cloud, utilizing the Discord API.

Discord Developer Documentation can be found on [Discord's Developer Portal](https://discord.com/developers/docs/intro).

# List of commands

**!hello** - Greets the user

**!quote** - Generates a random text blurb using one of Shakespeare's plays

**!write [text to save]** - Saves text that will be randomly selected when using the **!read** command. Can be erased using **!erase**.

**!read** - Randomly selects a text that was saved by **!write** and spits it out

**!erase [index position of saved text]** - Erases saved text at the specified index position

**!list** - Prints out a list of saved text in sequential order. Index position starts at 0.

**!wipe** - Wipes all saved text.

# Future plans

Using LSTM and deep learning with TensorFlow instead of Markov chains to generate text.

Making further use of Discord's API to add functionality to the bot.

