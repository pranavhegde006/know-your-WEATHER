import os
import discord
import requests 
import json
import datetime
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

def convert(seconds):
	seconds = seconds % (24 * 3600)
	hour = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60
	return "%d:%02d:%02d" % (hour, minutes, seconds)
	

def get_weather(location):
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
            rain1hrs = api_data['rain']['1h']
        else: 
            rain1hrs = "N/A"
        if 'clouds' in api_data:
            clouds = api_data['clouds']['all']
        else:
            clouds = "N/A"
        if 'snow' in api_data:
            snow1hrs = api_data['snow']['1h']
        else: 
            snow1hrs = "N/A"

        res = "Weather bot\n" + "Location: " + str(city) + "\n\n" + "Local time: " + str(time) + "\n" + "Temperature: " + str(current_temp) + "⁰C\n" + "Humidity: " + str(humidity) + "%\n" + "Rain volume for last hour: " + str(rain1hrs) + " mm\n" + "Wind speed: " + str(round(windSpeed*3.6, 2)) + "km/hr at " + str(windDirection) + "⁰\n" + "Snow volume for last hour: " + str(snow1hrs) + " mm\n" + "Cloudiness: " + str(clouds) + "%\n" + "Today's sunrise at " + str(sunrise) + " and sunset at " + str(sunset)
        
        return res


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


    
@client.event
async def on_ready():
    print("Bot {0.user} successfully logged in"
    .format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
      return

    if message.content.startswith('$hello'):
      await message.channel.send('Hello there ' + '!')

    if message.content.startswith('$weather'):
        if len(message.content) <= 9:
            await message.channel.send('@' + str(message.author) + " fetching the weather details for you.\n...")
            await message.channel.send("Inappropriate request recieved")
        
        else:
            await message.channel.send('@' + str(message.author) + " fetching the weather details for you.\n...")

            stri = message.content
            location = stri[9:]
            weather = get_weather(location)

            if weather == -1:
                await message.channel.send("Please enter valid location.")
            else : await message.channel.send(weather)

    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

my_secret = os.environ['TOKEN']

client.run(my_secret)
