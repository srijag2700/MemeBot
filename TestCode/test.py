import praw
import random

reddit = praw.Reddit(client_id='hJnubOcCq-kr6w', client_secret="is0O4mzC6XRF4EVxqpIBDCu-34E", 
    refresh_token = '458373337140-BOTNnk5sjEpX2KjL2Fs2jfSBvuM', user_agent='MemeBot')

memes = ['memes', 'dankmemes', 'MemeEconomy', '2meirl4meirl', 'me_irl', 'meme', 
    'surrealmemes', 'funny', 'trippinthroughtime', 'starterpacks', "ProgrammerHumor"]

submission = reddit.subreddit(random.choice(memes)).random()
print(submission.url)