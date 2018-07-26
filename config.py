from dataIO import fileIO
import os

false_strings = ["false", "False", "f", "F", "0", ""]

if fileIO("config.json", "check"):
    config = fileIO("config.json", "load")
else:
    config = {
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
        "username": os.environ["USERNAME"],
        "password": os.environ["PASSWORD"],
        "user_agent": os.environ["USER_AGENT"],
        "subreddit": os.environ["SUBREDDITS"].replace(" ", "").split(","),
        "users": os.environ["USERS"].lower().replace(" ", "").split(","),
        "bot_is_moderator": False if os.environ["BOT_IS_MODERATOR"] in false_strings else True,
        "store_size": int(os.environ["STORE_SIZE"]),
        "intro": os.environ["INTRO"]
    }