import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import json

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# dagens datum kan läggas till i url
def get_login_cred():
    with open('secrets.json') as f:
        temp = f.read()
        secrets = json.loads(temp)
        return secrets



def fetch_schedule(dag: int):
    dagens_datum = datetime.date.today() + timedelta(days=dag)
    dagens_datum = str(dagens_datum)[2:]

    url = 'https://webbschema.mdu.se/ajax/ajax_resursbokning.jsp?op=hamtaBokningar&datum='+dagens_datum+'&flik=FLIK_0001'
    login_url = 'https://webbschema.mdu.se/login_do.jsp'

    # logga in till kronox
    uname = get_login_cred()
    session = requests.session()
    session.post(login_url, data=uname)
    response = session.get(url).text

    soup = BeautifulSoup(response, 'html.parser')

    # hitta grupprum table
    grupprum_table = soup.find('table', class_='grupprum-table').get_text()

    spliced_grupprum = grupprum_table[79:].replace('platser,WB','').replace('WB','').replace('platser,', '').replace('platser', '').split()

    spliced_length = len(spliced_grupprum)

    booking_dict = {}
    room_index = []
    index_grupprum = 0

    #lägg till rumsnummer i dictionary samt key value lista
    #for i in range(0, 245):
    #    room_index.append(i*7)
    #    if i in room_index:
    #        booking_dict[spliced_grupprum[i][:6]] = []
    for i in spliced_grupprum:
        if i[0] == 'R' or i[0] == 'U':
            booking_dict[spliced_grupprum[index_grupprum][:6]] = []
            room_index.append(index_grupprum)
        index_grupprum += 1 

    #print(booking_dict)
    # fyll key value med dictionaries av tider
    for j in booking_dict:
        booking_dict[j].append({'08.15-10.00': 0})
        booking_dict[j].append({'10.15-12.00': 0})
        booking_dict[j].append({'12.15-14.00': 0})
        booking_dict[j].append({'14.15-16.00': 0})
        booking_dict[j].append({'16.15-18.00': 0})
        booking_dict[j].append({'18.15-20.00': 0})


    print(booking_dict)
    a = 0

    # fyll tider med student ID
    for i in booking_dict:
        if a in room_index:
            a += 1
        for j in range(0, 6):
            booking_dict[i][j] = spliced_grupprum[a]
            a += 1
    print(booking_dict)

    return booking_dict

@bot.command(name='bokat')
async def bokat(ctx, dag: int = 0):
    booking_dict = fetch_schedule(dag)

    medlemmar = ['', '', '', '', '', '']

    tider = ['08:15-10:00', '10:15-12:00', '12:15-14:00', '14:15-16:00', '16:15-18:00', '18:15-20:00']

    tid_index = 0


    #if medlemmar not in booking_dict:
        #message = "Inga bokade rum"
        #await ctx.send(message)
    for rum in booking_dict:
        for i in booking_dict[rum]:
            if i in medlemmar:
                message = f"Datum: {str(datetime.date.today() + timedelta(days=dag))[2:]}\nRum:     {rum}\nTid:        {tider[tid_index]}\nBokare: {i}\n".replace('','').replace('','').replace('','').replace('', '').replace('', '').replace('', '')
                await ctx.send(message)
                tid_index += 1

@bot.command(name='goodbot')
async def goodbot(ctx):
    await ctx.send('https://giphy.com/gifs/theoffice-ZfK4cXKJTTay1Ava29')
fetch_schedule(1)
# Run the bot with your token
if __name__ == "__main__":
    bot.run('')
