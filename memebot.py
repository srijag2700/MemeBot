import discord
from discord.ext import commands
import random
import praw
import datetime
import time
import os
from dotenv import load_dotenv

description = '''A bot solely for memes.'''
bot = commands.Bot(command_prefix='m!', description=description)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
redditID = os.getenv('REDDIT_ID')
reddit_secret = os.getenv('REDDIT_SECRET')
reddit_refresh = os.getenv('REDDIT_REFRESH')

reddit = praw.Reddit(client_id=redditID, client_secret=reddit_secret, 
    refresh_token = reddit_refresh, user_agent='MemeBot')

memes = ['memes', 'dankmemes', 'MemeEconomy', '2meirl4meirl', 'me_irl', 'meme', 
    'surrealmemes', 'funny', 'trippinthroughtime', 'starterpacks', "ProgrammerHumor"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def meme(ctx):
    sub = reddit.subreddit(random.choice(memes))
    submission = sub.random()
    await ctx.send(submission.url + " from " + sub.display_name)

"""@bot.command()
async def memes(ctx, num: int):
    xNum = num
    for x in range (xNum):
        sub = reddit.subreddit(random.choice(memes)).random()
        await ctx.send(sub.url)"""

@bot.command()
async def info(ctx):
    await ctx.send(description)

@bot.event
async def memeOfTheHour(ctx):
    if datetime.time().minute == 0:
        submission = reddit.subreddit(random.choice(memes)).random()
        await ctx.send('Meme Of The Hour: ' + submission.url)

bot.run(token)