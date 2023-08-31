import discord
import os
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()


Discord_TOKEN = os.getenv("TOKEN")
intent = discord.Intents.default()
intent.message_content = True
client = discord.Client(command_prefix = '!', intents = intent)

def market_is_open():
    today = datetime.date.today()
    weekday = today.weekday()
    current_datetime = datetime.datetime.now()
    current_time = str(current_datetime.time())
    if(current_time[0]!="0"):
        hour = int(current_time[0:2])
    else:
        hour = int(current_time[1])

    if(current_time[3]!="0"):
        minute = int(current_time[3:5])
    else:
        minute = int(current_time[4])

    if((0<=weekday<=4)&(9<=hour<=3)):
        return True
    elif((hour==4)&(minute==0)):
        return True
    else:
        return False
    

def get_previous_market_day():
    today = datetime.date.today()
    weekday = today.weekday()

    # If today is Monday, get data for Friday (weekday 4)
    if weekday == 0:
        days_to_subtract = 3
    # If today is Sunday, get data for Friday (weekday 4)
    elif weekday == 6:
        days_to_subtract = 2
    # Otherwise, get data for the previous day
    else:
        days_to_subtract = 1

    previous_market_day = today - datetime.timedelta(days=days_to_subtract)
    return str(previous_market_day) + " 16:00:00"

def get_previous_close_price():
    previous_day = get_previous_market_day()
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=HDNZAJO3127837JB'
    response = requests.get(url)
    data = response.json()
    previous_close = data['Time Series (5min)'][str(previous_day)]['4. close']
    return previous_close

def gettime():
    current_datetime = datetime.datetime.now()
    date = str(current_datetime)
    current_time = str(current_datetime.time())
    time = current_time[0:6] + "00"



@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    message_content = message.content
    if message_content==('!hi'):
        await message.channel.send("Hello user")
    #elif message_content==("!IBM"):
    else:
        if(market_is_open()):
            today_date = gettime
            key = "HDNZAJO3127837JB"
            #symbol = message_content[1:]
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey={key}'
            response = requests.get(url)
            data = response.json()
            timeseries = data.get('Time Series (5min)')
            recent =timeseries[today_date]
            await message.channel.send(recent)
        else:
            await message.channel.send(f"The market is closed. The closing price is: {get_previous_close_price()}")

#print(datetime.date.today().strftime('%Y-%m-%d %H:%M:%S'))


client.run(Discord_TOKEN)