import os
import discord
import requests
import json
import random
from weather import *
from discord.ext import commands

client = discord.Client()
token = os.environ['TOKEN']
api_key = os.environ['api_key']
sad_words = ["sad","depressed","unhappy","depressed","miserable"]

starter_encoragements = ["cheer up!","It's fine","Hang in there","You are a great person"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "   -->" + json_data[0]['a']
  return(quote)

 
@client.event
async def on_ready():
  print('We have been logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name= 'w.[location]'))

#msg = message.content

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    if message.content.startswith('$hi'):
      await message.channel.send('Hi there! wassup')

    if message.content.startswith('$hey buddy'):
      await message.channel.send('Hello there!')

    if message.content.startswith('$kg dei?'):
      await message.channel.send('Hey karthik where r u?')

    if message.content.startswith('$quote'):
      quote = get_quote()
      await message.channel.send(quote)

    if message.content.startswith('$help'):
      await message.channel.send('$hi , $hey buddy , $kg dei? ,     $quote')

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(starter_encoragements))

    if message.content.startswith('w.'):
      await message.channel.send('The weather report will update in a sec :)')
      location = message.content.replace('w.','').lower()
      if len(message.content.replace('w.', '')) >= 1:
        location = message.content.replace('w.', '').lower()
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
        try:
            data = parse_data(json.loads(requests.get(url).content)['main'])
            await message.channel.send(embed=weather_message(data, location))
        except KeyError:
            await message.channel.send(embed=error_message(location))


  async def play(ctx , url :str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
  
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voiceChannel.connect()  


client.run(token)