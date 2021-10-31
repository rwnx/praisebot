import tweepy
import os
import sys
import re
import logging
import random

LOG_LEVEL = os.environ.get("LOG_LEVEL") or logging.INFO
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_KEY_TOKEN = os.environ["ACCESS_KEY_TOKEN"]
ACCESS_KEY_SECRET = os.environ["ACCESS_KEY_SECRET"]

logging.basicConfig(stream=sys.stderr, level=LOG_LEVEL)

logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY_TOKEN, ACCESS_KEY_SECRET)

api = tweepy.API(auth)

logger.info("Connecting to Twitter API...")
bot_user = api.verify_credentials()
me = bot_user.name

praises = [
  "you're the best 👏👏👏",
  "you are incredible! 😇",
  "you are majestic ✨✨✨",
  "please continue to be fantastic ✨",
  "your presence brings us joy ⭐️",
  "don't you need a license for that level of awesomeness? ✨",
  "you light up the room 💡",
  "you are way cool",
  "you were cool before cool was a thing",
  "you are appreciated! 🌟",
  "you're better than a triple-scoop ice cream. 🍦 (with sprinkles)",
]

def praise(target):
  praise = random.sample(praises, 1)[0]

  praise_tweet = f"@{target} {praise}"
  logger.info("praising: %s", praise_tweet)
  api.update_status(praise_tweet)

class PraiseStream(tweepy.Stream):
    def on_status(self, status):
      logger.info("@%s >> %s", status.user.screen_name, status.text)
      if re.search(r"\s+praise\s+me\s*$", status.text):
        praise(status.user.screen_name)

      for mention in re.finditer(r"\s@(\w+)\b", status.text):
          target = mention.group(1)
          if target == me:
            continue
          
          praise(target)

logger.info(f"Connected as @{bot_user.screen_name}")

mention_streams = PraiseStream(API_KEY, API_SECRET, ACCESS_KEY_TOKEN, ACCESS_KEY_SECRET)
mention_streams.filter(track=[f"@{bot_user.screen_name}"])