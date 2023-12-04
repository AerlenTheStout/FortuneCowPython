import discord
from os import system, path
from io import StringIO
from subprocess import getoutput
import sys
from random import randrange
from PIL import Image, ImageDraw, ImageFont
from math import ceil

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Fortune Bot has logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for !fortune'))
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #print(str(message))

    #print(message.content)
    if (message.content.find('!fortune') != -1):


        # Use our choice to generate a cowsay
        msg = getoutput('/usr/games/fortune | /usr/games/cowsay')+'\n'
        #print(msg)
        # Image generation: calculate length and width of image and instantiate
        msgFont = ImageFont.truetype("UbuntuMono-R.ttf", 12)

        left, top, right, bottom = ImageDraw.Draw(Image.new('RGB',  (500, 5000))).multiline_textbbox((0,0), msg, font=msgFont)  #msgFont.getbbox(substring)
        #print('bottom:%d, top:%d'%(bottom, top))
        width, height = (right - left)+32, (bottom - top)+20
        #print('width:%d,height:%d'%( width, height))

        msgImg = Image.new('RGB', (width,height), (255, 255, 255))

        msgDraw = ImageDraw.Draw(msgImg)

        msgDraw.multiline_text((16, 0), msg, fill='black', font=msgFont)
        # TODO: Don't save to hard drive just to load again
        msgImg.save('/tmp/fortune.png')
        await message.channel.send(file=discord.File('/tmp/fortune.png'))

# Yeah nah not letting you lot see my ~ultra secret~ Discord Token(tm)
tokFile = open(path.join(path.dirname(path.realpath(__file__)),'.env'))
DISCORD_TOKEN = tokFile.read()
tokFile.close()
client.run(DISCORD_TOKEN)

