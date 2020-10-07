# bot.py
import os
import discord
from PIL import Image
import io
import urllib.request as urllib
import random as random
##from discord.ext import bot
##TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = 'NzYyNzY0OTYwODQ1MDA0ODUx.X3t6Og.CCu7deCrtrYA0pnLwjLR3Tf4FI8'
GUILD = '760098399869206529'
client = discord.Client()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
class DiscordBot():
    

    @client.event
    async def on_ready():
        
        print(
            client.user
        )

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith('|test'):
            await message.channel.send("success")
            
    @client.event
    async def on_raw_reaction_add(payload):

##        if payload.channel_id==763016400872013834:
##            channel = client.get_channel(763016400872013834)
##            message = await channel.fetch_message(payload.message_id)
##            reaction = discord.utils.get(message.reactions, emoji="✅")
##            if reaction.count==1:
##                url=message.attachments[0].url.replace("https","http")
##                request=urllib.request(url)
##                im = Image.open(urllib.urlopen(request))
##                bytes_array = io.BytesIO()
##                im.save(bytes_array)
##                bytes_array = bytes_array.getvalue()
##                print(url)
##                print(bytes_array)
##                await message.guild.create_custom_emoji(name=str(random.randint(0,99)), image = data)
##                

        if payload.message_id == 763433157516066846:
            ##await client.get_channel(payload.channel_id).send("hai")
            if payload.emoji.name == "✅":
                await payload.member.add_roles(client.get_guild(payload.guild_id).get_role(762809681634132018))
                print(payload.member.name + " Has just agreed")
                ##do the thing
            elif payload.emoji.name == "❌":
                await payload.member.edit(nick="I can't follow rules")
        

    @client.event
    async def on_raw_reaction_remove(payload):
        if payload.message_id == 763433157516066846:
            guild=client.guilds[0]
            if payload.emoji.name == "✅":
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(762809681634132018))
            elif payload.emoji.name == "❌":
                await guild.get_member(payload.user_id).edit(nick=None)



    
client.run(TOKEN)
