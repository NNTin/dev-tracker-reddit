import praw
import re
from data import ThreadData
from config import config
from collections import deque
from datetime import datetime
from urllib.parse import quote_plus

if __name__ == '__main__':
    r = praw.Reddit(client_id=config["client_id"],
                    client_secret=config["client_secret"],
                    password=config["password"],
                    user_agent=config["user_agent"],
                    username=config["username"])

    # the most recent threads a dev has replied in
    recent_threads = deque(maxlen=config["store_size"])

    subreddit = r.subreddit("+".join(config["subreddit"]))

    for comment in subreddit.stream.comments():
        try:
            comment_author = comment.author.name.lower()
        except AttributeError:
            # author is deleted, don't care about this comment
            continue

        intro_template = config["intro"]
        intro = intro_template.format(bot_name=r.config.username,
                                      subreddit=str(comment.subreddit),
                                      users=", ".join(config["users"]))

        subreddit_url_encoded = quote_plus("/r/{subreddit}".format(subreddit=str(comment.subreddit)))

        outtro_template = "[source](https://github.com/NNTin/dev-tracker-bot) on GitHub, " \
                          "[message](https://www.reddit.com/message/compose?to={url}) " \
                          "the moderators"
        outtro = outtro_template.format(bot_name=r.config.username,
                                        subreddit=str(comment.subreddit),
                                        users=", ".join(config["users"]),
                                        url=subreddit_url_encoded)

        outtro = " " + outtro
        outtro = " ^^".join(outtro.split(" "))

        if comment_author in config["users"]:
            submission_id = comment.submission.fullname

            bot_comment_exist = submission_id in map(lambda x: x.submission_id, recent_threads)

            if bot_comment_exist:
                print("[A] {author}: {link}".format(author=comment.author.name,
                                                    link="https://dm.reddit.com" + comment.permalink))
            else:
                print("[N] {author}: {link}".format(author=comment.author.name,
                                                    link="https://dm.reddit.com" + comment.permalink))
            old_comments = ""

            if bot_comment_exist:
                regex = r"(?P<fullmatch>\* \[Comment by (?P<redditname>\w+)\]\(\/r\/(?P<subreddit>\w+)\/comments" \
                        r"\/(?P<submissionid>\w+)\/\w*\/(?P<commentid>\w+)\/\?context=\d+(?P<hasnote> \"(?P<note>.+)" \
                        r"\")?\):\n\n(?P<message>( >.+\n)+))"

                data = next(filter(lambda x: x.submission_id == submission_id, recent_threads)).dict()
                comment_id = data["comment_id"]
                bot_comment = next(r.info([comment_id]))

                matches = re.finditer(regex, bot_comment.body, re.MULTILINE)

                for match in matches:
                    old_comments += match["fullmatch"] + "\n"

            header_template = '* [Comment by {user_name}]({permalink}?context=9 "posted on {datetime}"):\n'

            header = header_template.format(user_name=comment.author.name,
                                            permalink=comment.permalink,
                                            datetime=str(datetime.utcfromtimestamp(
                                                comment.created_utc)) + " UTC")

            quote = "\n" + comment.body
            quote = "\n > ".join(quote.split("\n"))

            new_comment = header + quote

            reply = intro + "\n\n" + old_comments + new_comment + "\n\n---\n\n" + outtro

            if bot_comment_exist:
                bot_comment.edit(reply)
                continue

            else:
                bot_comment = comment.submission.reply(reply)
                comment_id = bot_comment.fullname
                recent_threads.append(ThreadData(submission_id=submission_id,
                                                 comment_id=comment_id))
                continue


