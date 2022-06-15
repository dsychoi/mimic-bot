from replit import db

class Quote:
  def store_quote(self, quote):
    """ Stores a quote inside of the Replit database """
    if "quotes" in db.keys():
      quotes = db["quotes"]
      quotes.append(quote)
      db["quotes"] = quotes
    else:
      db["quotes"] = [quote]
  
  
  def delete_quote(self, index):
    """ Deletes a quote from the Replit database at the specified index """
    quotes = db["quotes"]
    if len(quotes) > index:
      del quotes[index]
      db["quotes"] = quotes