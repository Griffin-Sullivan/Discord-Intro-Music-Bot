import os
import json

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

with open('user-intros.txt') as json_file:
    data = json.load(json_file)
    for p in data['intros']:
        print(f"{p['name']} = {p['song']}")

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print (
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == '$':
        user_song = message.content[7:].title()
        response = f'{message.author} has set their intro song as "{user_song}"'
        user = str (message.author)
        
        if len(data['intros']) > 0:
            for i in range(len(data['intros'])):
                if data['intros'][i]['name'] == user:
                    if data['intros'][i]['song'] != user_song:
                        data['intros'][i]['song'] = user_song
                else:
                    data['intros'].append({
                        "name": user,
                        "song": user_song
                    })
        else:
            data['intros'].append({
                "name": user,
                "song": user_song
            })
        with open('user-intros.txt', 'w') as outfile:
            json.dump(data, outfile)
        await message.channel.send(response)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        for i in data['intros']:
            if i['name'] == str (member):
                play_song = f"-play {i['song']}"
        await member.guild.system_channel.send(play_song)

client.run(TOKEN)
