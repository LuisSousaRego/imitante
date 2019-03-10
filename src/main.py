import praw
import re


def getPortugal():
    user_agent = "linux:imitante:v0.0.1 (by /u/imitante)"
    reddit = praw.Reddit('imitante', user_agent=user_agent)
    return reddit.subreddit('portugal')

def removeLinks(text):
    regex = r"\[(.+)]\(http.+\)"
    subst = "\\1"
    result = re.sub(regex, subst, text, 0, re.IGNORECASE)
    return result

portugal = getPortugal()
palavras = set()

for submission in portugal.hot(limit=10):
    if submission.is_self:
        palavras = {post for post in removeLinks(submission.selftext).split()}

print(palavras)


