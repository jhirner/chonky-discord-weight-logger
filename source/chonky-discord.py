import os
import discord
from dotenv import load_dotenv
from random import choice
import dataset
from datetime import datetime

# Load credentials and create the client.
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER = os.getenv("DISCORD_SERVER")
DEV_CHANNEL = os.getenv("DISCORD_DEV_CHANNEL_ID")
DB_PATH = os.getenv("PATH_TO_DB")
client = discord.Client()


def update_db(person, weight):
    # When called, update the SQLite database.
    new_entry = {"person" : person,
                 "weight" : weight,
                 "datetime" : datetime.now()}
    db_table = "weights"
    with dataset.connect("sqlite:///" + DB_PATH) as db:
        db[db_table].insert(new_entry)
    return


## Define events.

# When logging into the Discord server.
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            # Post a message to Development channel.
            # The two lines below don't quite work.
            # dev_chan = client.get_channel(DEV_CHANNEL)
            # await dev_chan.send("Chonky in the house!")
            break
            
# When a message is received            
@client.event
async def on_message(message):
    
    # Don't let the bot respond to its own messages.
    if message.author == client.user:
        return
    
    confirmations = ["Message received.",
                     "Understood.",
                     "You betcha.",
                     "I'm on it.",
                     "Roger roger.",
                     "10-4, buddy.",
                     "Okay, thanks.",
                     "Affirmative."]
    
    # Determine if the message is a valid number.
    # Inform the sender whether the input was accepted.
    try:
        new_weight = float(message.content)
        if new_weight > 0:
            response = choice(confirmations)
            person_to_update = message.channel.name
            update_db(person_to_update, new_weight)
        else:
            response = "Negative numbers are not allowed. Neither is zero, you liar."
    except ValueError:
        response = "I didn't get that. Please send only numbers."
    await message.channel.send(response)

client.run(TOKEN)
