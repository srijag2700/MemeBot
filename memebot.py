import discord
from discord.ext import commands
import random
import praw
import datetime
import time
import os
from dotenv import load_dotenv

description = '''A bot solely for memes, created by <@!144266578408636417>. \nm!meme: Send a random meme from Reddit. \nm!mfrom <subreddit>: Send a meme from the specified subreddit.'''
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

    game = discord.Game("with memes | m!info")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def meme(ctx):
    sub = reddit.subreddit(random.choice(memes))
    submission = sub.random()
    await ctx.send(submission.url + " from r/" + sub.display_name)

def subreddit_validate(temp: str):
    sub_exists = True
    sub = reddit.subreddit(temp)
    try:
        sub._fetch()
    except:
        sub_exists = False
    return sub_exists
        

@bot.command()
async def mfrom(ctx, newSub: str):
    if (subreddit_validate(newSub)):
        sub = reddit.subreddit(newSub)
        if (sub.over18 == True):
            await ctx.send("NSFW subreddit detected. Nice try :)")
        else:
            submission = sub.random()
            await ctx.send(submission.url + " from r/" + sub.display_name)
    else:
        await ctx.send("Subreddit does not exist. Please enter an existing subreddit & make sure your capitalization is correct.")

"""@bot.command()
async def memes(ctx, num: int):
    xNum = num
    for x in range (xNum):
        sub = reddit.subreddit(random.choice(memes)).random()
        await ctx.send(sub.url)"""

@bot.event
async def on_message(message):
    if bot.user.id != message.author.id:
        if 'srija' in message.content.lower():
            await message.channel.send('did someone say srija')

    await bot.process_commands(message)

@bot.command()
async def info(ctx):
    await ctx.send(description)
    
@bot.command()
async def invite(ctx):
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=684952708830330910&permissions=68608&scope=bot")

@bot.command()
async def servers(ctx):
    await ctx.send("I am in " + str(len(bot.guilds)) + " servers.")

@bot.event
async def memeOfTheHour(ctx):
    if datetime.time().minute == 0:
        sub = reddit.subreddit(random.choice(memes))
        submission = sub.random()
        await ctx.send('Meme Of The Hour: ' + submission.url + " from r/" + sub.display_name)

bot.run(token)