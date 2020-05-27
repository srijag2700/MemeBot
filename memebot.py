import discord
from discord.ext import commands
import random
import praw
import datetime
import time
import os
from dotenv import load_dotenv

description = 'A bot solely for memes, created by Srija (<@!144266578408636417>). \nm!meme: Sends a random meme from Reddit. \nm!mfrom <subreddit>: Sends a meme from the specified subreddit. \nm!invite: Invite me to your own server. \nm!servers: See how many servers I\'m in.'
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

pastas = ['copypasta', 'emojipasta', 'WholesomeCopypasta']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    game = discord.Game("with memes | m!info")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command(description="Sends a random meme from Reddit.")
async def meme(ctx):
    sub = reddit.subreddit(random.choice(memes))
    submission = sub.random()
    while (submission.over_18 == True):
        submission = sub.random()
    await ctx.send(submission.url + " from r/" + sub.display_name)

@bot.command(description='Sends a random copypasta from Reddit.')
async def pasta(ctx):
    sub = reddit.subreddit(random.choice(pastas))
    submission = sub.random()
    while (submission.over_18 == True or len(submission.selftext) >= 2000):
        submission = sub.random()
    await ctx.send("From r/" + sub.display_name + "\n\n" + submission.selftext)

def subreddit_validate(temp: str):
    sub_exists = True
    sub = reddit.subreddit(temp)
    try:
        sub._fetch()
    except:
        sub_exists = False
    return sub_exists 

@bot.command(description="Sends a meme from the specified subreddit.")
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

@bot.command(description="Information about MemeBot.")
async def info(ctx):
    await ctx.send(description)
    
@bot.command(description="Invite the bot to your own server.")
async def invite(ctx):
    await ctx.send("<https://discordapp.com/oauth2/authorize?client_id=684952708830330910&permissions=68608&scope=bot>")

@bot.command(description="Number of servers the bot is in.")
async def servers(ctx):
    await ctx.send("I am in " + str(len(bot.guilds)) + " servers.")

@bot.event
async def on_message(message):
    if bot.user.id != message.author.id and message.author.id == 709835785821487154:
        await message.channel.send('cute dog')
    elif bot.user.id != message.author.id and message.author.bot == False:
        if 'srija' in message.content.lower():
            await message.channel.send('did someone say srija')

    await bot.process_commands(message)

"""@bot.command()
async def memes(ctx, num: int):
    xNum = num
    for x in range (xNum):
        sub = reddit.subreddit(random.choice(memes)).random()
        await ctx.send(sub.url)

@bot.event
async def memeOfTheHour(ctx):
    if datetime.time().minute == 0:
        sub = reddit.subreddit(random.choice(memes))
        submission = sub.random()
        await ctx.send('Meme Of The Hour: ' + submission.url + " from r/" + sub.display_name)"""

bot.run(token)