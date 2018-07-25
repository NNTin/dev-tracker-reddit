

class ThreadData:
    def __init__(self, submission_id, comment_id):
        self.submission_id = submission_id  # thread with a dev having replied
        self.comment_id = comment_id    # the bot's own comment id

    def dict(self):
        return {
            "submission_id": self.submission_id,
            "comment_id": self.comment_id
        }

