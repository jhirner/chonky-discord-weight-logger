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

def delete_prev(person):
    # When called, find the most recent weight logged
    # in this channel and delete it.
    db_table = "weights"
    
    query_templ = "SELECT id, weight, MAX(datetime) from {} WHERE person = '{}'" 
    query_str = query_templ.format(db_table, person)
    
    with dataset.connect("sqlite:///" + DB_PATH) as db:
        # Get the ID number of the most recent entry for the given
        # person/channel, then delete the dabase entry with that ID.
        entry_to_del = list(db.query(query_str))[0]
        id_to_del = entry_to_del["id"]
        wt_to_del = entry_to_del["weight"]
        del_from_datetime = entry_to_del["MAX(datetime)"]
        
        db[db_table].delete(id = id_to_del)
        
        deletion_msg = "Deleted entry: {wt} pounds entered at {dt}".format(
            wt = wt_to_del,
            dt = del_from_datetime)
    
    return deletion_msg


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
    
    person_to_update = message.channel.name
    
    confirmations = ["Message received.",
                     "Understood.",
                     "You betcha.",
                     "I'm on it.",
                     "Roger roger.",
                     "10-4, buddy.",
                     "Okay, thanks.",
                     "Affirmative."]
    
    if message.content == "undo":
        # Sending 'undo' will delete the most recent entry.
        delete_msg = delete_prev(person_to_update)
        await(message.channel.send(delete_msg))
        
    else:
        # Determine if the message is a valid number.
        # Inform the sender whether the input was accepted.
        try:
            new_weight = float(message.content)
            if new_weight > 0:
                response = choice(confirmations)                
                update_db(person_to_update, new_weight)
            else:
                response = "Negative numbers are not allowed. Neither is zero, you liar."
        except ValueError:
            response = "I didn't get that. Please send only numbers."
        await message.channel.send(response)

client.run(TOKEN)
