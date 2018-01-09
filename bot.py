import tweepy
import os
import pickle
import discord
import asyncio
import logging
import re

auth=tweepy.OAuthHandler("w1eFQDLLUgz1w6MXideNBUUuv","BkPviFYTxmy2GJnZCa2oHaiAW66wg2RxBcLjr5SjE3vU0XBw0s")

logging.basicConfig(level=logging.ERROR)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content == "tb:connect":
        if os.path.exists("{}.txt".format(message.author.id)) == True:
            await client.send_message(message.author, "You are already logged on.")
        else:
            await client.send_message(message.author, "Login to twitter")
            await client.send_message(message.author, "Connect to your twitter account with the link below and send me the PIN Twitter will give you")
            auth=tweepy.OAuthHandler("w1eFQDLLUgz1w6MXideNBUUuv","BkPviFYTxmy2GJnZCa2oHaiAW66wg2RxBcLjr5SjE3vU0XBw0s")
            url = auth.get_authorization_url()
            await client.send_message(message.author, url)
            pin = await client.wait_for_message(author = message.author)
            pin = pin.content
            auth.get_access_token(pin)
            with open("{}.txt".format(message.author.id), "wb") as codes:
                pickle.dump([auth.access_token, auth.access_token_secret], codes)
            await client.send_message(message.author.id, "Done!")

    if "twitter.com" in message.content and "status" in message.content:
        await client.add_reaction(message, u'\U0001f501')
        await client.add_reaction(message, u'\U00002764')

@client.event
async def on_reaction_add(reaction, user):
    if "twitter.com" in reaction.message.content and "status" in reaction.message.content:
        if os.path.exists("{}.txt".format(user.id)) == True:
            if user.bot == False and reaction.emoji == u'\U0001f501':
                with open("{}.txt".format(user.id), "rb") as codes:
                    a = pickle.load(codes)
                    auth.set_access_token(a[0], a[1])
                    stas = re.search("(?:status\/)(\d+)", reaction.message.content)
                    stas = stas.group(1)
                    print(stas)
                    # stas = reaction.message.content.split("/")[-1]
                    api = tweepy.API(auth)
                    api.verify_credentials()
                    api.retweet(stas)
                        
            if user.bot == False and reaction.emoji == u'\U00002764':
                with open("{}.txt".format(user.id), "rb") as codes:
                    a = pickle.load(codes)
                    auth.set_access_token(a[0], a[1])
                    stas = re.search("(?:status\/)(\d+)", reaction.message.content)
                    stas = stas.group(1)
                    print(stas)
                    # stas = reaction.message.content.split("/")[-1]
                    api = tweepy.API(auth)
                    api.verify_credentials()
                    api.create_favorite(stas)
        else:
            await client.send_message(user, "You are not logged on: to log in, send tb:connect")

@client.event
async def on_reaction_remove(reaction, user):
    if "twitter.com" in reaction.message.content and "status" in reaction.message.content:                    
        if user.bot == False and reaction.emoji == u'\U00002764':
            if os.path.exists("{}.txt".format(user.id)) == True:
                with open("{}.txt".format(user.id), "rb") as codes:
                    a = pickle.load(codes)
                    auth.set_access_token(a[0], a[1])
                    stas = re.search("(?:status\/)(\d+)", reaction.message.content)
                    stas = stas.group(1)
                    api = tweepy.API(auth)
                    api.verify_credentials()
                    api.destroy_favorite(stas)
                    
client.run('MzQwOTMwODEzMDQ4NzgyODU4.DF5sGg.ByXoRpgJEMXk1Z5V2RyoJiHzPFE')
