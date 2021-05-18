import os
import discord
import requests 
import json
from dotenv import load_dotenv
import datetime
from datetime import timezone
import random

load_dotenv()

client = discord.Client()

images = [
    'https://images.unsplash.com/photo-1526750925531-9e8fdbf95de3?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=967&q=80',
    'https://images.unsplash.com/photo-1491234323906-4f056ca415bc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=967&q=80',
    'https://images.unsplash.com/photo-1500534623283-312aade485b7?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/photo-1515858168371-d8f5843eb9bd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/38/L2NfDz5SOm7Gbf755qpw_DSCF0490.jpg?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/photo-1474452926969-af7bfdb9ca39?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1189&q=80',
    'https://images.unsplash.com/photo-1474575767135-14237cca19dc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/photo-1446160657592-4782fb76fb99?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1049&q=80',
    'https://images.unsplash.com/reserve/RONyPwknRQOO3ag4xf3R_Kinsey.jpg?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/photo-1465188162913-8fb5709d6d57?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1050&q=80'
    ]


def convert(seconds):
	seconds = seconds % (24 * 3600)
	hour = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60
	return "%d:%02d:%02d" % (hour, minutes, seconds)
	

def get_weather(message, location):
    weather_api = os.environ['weather_key']
    api_call_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+weather_api
    api_link = requests.get(api_call_link)
    if api_link.status_code != 200:
        return -1
    else:
        api_data = api_link.json()

        current_temp = round(api_data["main"]['temp'] - 273)
        humidity = api_data["main"]['humidity']
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        timeShift = api_data['timezone']
        time = convert(utc_timestamp + timeShift)
        city = api_data['name'] + ', ' + api_data['sys']['country']
        sunrise = convert(api_data['sys']['sunrise'] + timeShift)
        sunset = convert(api_data['sys']['sunset'] + timeShift)
        windSpeed = api_data['wind']['speed']
        windDirection = api_data['wind']['deg']
        if 'rain' in api_data:
            rain1hrs = str(api_data['rain']['1h']) + 'mm'
        else: 
            rain1hrs = "N/A"
        if 'clouds' in api_data:
            clouds = str(api_data['clouds']['all']) + '%'
        else:
            clouds = "N/A"
        if 'snow' in api_data:
            snow1hrs = str(api_data['snow']['1h']) + '%'
        else: 
            snow1hrs = "N/A"
        
        res = discord.Embed(title='Know your weather 🌦', description=str(city), color=0x0048CD)
        res.add_field(name='Local time', value=str(time), inline=False)
        res.add_field(name='Temperature', value=str(current_temp) + '⁰C', inline=True)
        res.add_field(name='Humidity', value=str(humidity) + '%', inline=True)
        res.add_field(name='Wind speed', value=str(windSpeed)+'km/hr at ' + str(windDirection) + '⁰', inline=True)
        res.add_field(name='Cloudiness', value=clouds, inline=True)
        res.add_field(name='Rain volume for the past hour', value=rain1hrs, inline=False)
        res.add_field(name='Snow volume for the past hour', value=snow1hrs, inline=False)
        res.add_field(name='Sunrise today', value=str(sunrise), inline=True)
        res.add_field(name='Sunset today', value=str(sunset), inline=True)
        res.add_field(name='Weather report requested by ', value=str(message.author)[:-5], inline=False)
        return res



@client.event
async def on_ready():
    print("Bot {0.user} successfully logged in"
    .format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
      return

    if message.content.startswith('$hello'):
        embedVar = discord.Embed(title="Welcome to Know your Weather! 🌦", description='Use **$help** command for more.', color=0xFFA500)
        embedVar.add_field(name = 'Project', value = 'https://github.com/pranavhegde006/know-your-weather', inline=False)
        embedVar.set_author(name="Pranav Hegde")
        await message.channel.send(embed=embedVar)
    
    if(message.content.startswith('$ping')):
        embedVar = discord.Embed(title='Know your weather 🌦', description = "It's never too **late**!", color=0xff0000)
        embedVar.add_field(name = '**PONG**', value=str(round(client.latency * 1000)) + 'ms', inline=False)
        embedVar.add_field(name = '**$help**', value = 'Use $help command for more info.', inline=False)
        await message.channel.send(embed = embedVar)

    if(message.content.startswith('$help')):
        res = discord.Embed(title='Know your weather 🌦', description='I hope you find some useful commands here!', color=0xffffff)
        res.add_field(name = '**$weather \{city_name\}**', value='This command fetches you the real time weather report of the city you enter. \nE.g.  $weather bangalore', inline=False)
        res.add_field(name = '**$inspire**', value = 'Use $inspire to get some great, thought provoking quotes!', inline=False)
        res.add_field(name = '**$ping**', value = 'Use $ping to know bot latency.', inline=False)
        res.add_field(name = '**$help**', value = 'Well this is the command you are using right now xD. It gives you a brief capabilities of the bot.', inline=False)
        res.add_field(name = '**$hello**', value='Use $hello to know about project details and more.', inline=False)
        await message.channel.send(embed = res)

    if message.content.startswith('$inspire'):
      img_link = random.choice(images)
      response = requests.get("https://zenquotes.io/api/random")
      json_data = json.loads(response.text)
      embedVar = discord.Embed(title = str(json_data[0]['q']), description = str(json_data[0]['a']), color=0xffff00)
      embedVar.add_field(name = '**$help**', value='Use $help command for more info', inline=False)
      embedVar.set_author(name="Quote!")
      embedVar.set_image(url= img_link)
      await message.channel.send(embed=embedVar)
    
    if message.content.startswith('$weather'):
        if len(message.content) <= 9:
            await message.channel.send("Inappropriate request recieved")
        
        else:
            stri = message.content
            location = stri[9:]

            await message.channel.send(message.author.mention + ", hold tight! Fetching the weather report of " + location + " for you.\n...")
            weather = get_weather(message, location)

            if weather == -1:
                await message.channel.send("Please enter valid location.")

            else : 
                await message.channel.send(embed=weather)
    if message.content.startswith('$servers'):
        if(message.author.id == 660695048471707660):
            dat = 'I\'m currently present in: \n'
            guilds_details = await client.fetch_guilds(limit=150).flatten()
            count = 1
            for guild_deets in guilds_details:
                dat += f"\t\t {count}. {guild_deets.name}\n"
                count += 1
            await message.channel.send(dat)
        else: 
            await message.channel.send('Say whaaat?')


my_secret = os.environ['TOKEN']

client.run(my_secret)
