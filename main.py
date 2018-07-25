import praw
import re
from data import ThreadData
from config import config
from collections import deque


# note: use deque to store the most recent 100 messages


if __name__ == '__main__':
    r = praw.Reddit(client_id=config["client_id"],
                    client_secret=config["client_secret"],
                    password=config["password"],
                    user_agent=config["user_agent"],
                    username=config["username"])

    # the most recent threads a dev has replied in
    recent_threads = deque(maxlen=config["store_size"])

    subreddit = r.subreddit("+".join(config["subreddit"]))
    #subreddit = r.subreddit("all")

    for comment in subreddit.stream.comments():
        try:
            comment_author = comment.author.name.lower()
        except AttributeError:
            # author is deleted, don't care about this comment
            continue

        if comment_author in config["users"]:
            submission_id = comment.submission.fullname

            if submission_id in map(lambda x: x.submission_id, recent_threads):
                # todo: apply regex and get old message

                regex = r"\* \[Comment by (?P<redditname>\w+)\]\(\/r\/(?P<subreddit>\w+)\/comments\/" \
                        r"(?P<submissionid>\w+)\/\w*\/(?P<commentid>\w+)\/\?context=\d+(?P<hasnote> \"" \
                        r"(?P<note>.+)\")?\):\n\n(?P<message>( >.+\n)+)"

                print('Path One')
                data = next(filter(lambda x: x.submission_id == submission_id, recent_threads)).dict()
                print(data)
                comment_id = data["comment_id"]
                print(comment_id)
                bot_comment = next(r.info([comment_id]))
                print(bot_comment.body)

                bot_comment.edit("Echo2: " + comment.body)
            else:
                print('Path Two')

                comment_by_template = '* [Comment by {user_name](/r/{subreddit_name/comments/{submission_id}//' \
                                      '{comment_id}/?context=9 "posted on {datetime}"):\n'

                comment_by = comment_by_template.format(user_name="placeholder",
                                                        subreddit="placeholder",
                                                        submission_id=str(comment.submission),
                                                        comment_id=str(comment),
                                                        datetime="placeholder")

                quote = "\n > " + comment.body
                quote = "\n > ".join(quote.split("\n"))

                reply = quote


                comment_id = bot_comment.fullname
                recent_threads.append(ThreadData(submission_id=submission_id,
                                                 comment_id=comment_id))

                bot_comment = comment.submission.reply(reply)
                print(reply)

                break # todo: remove

