import praw

user_agent = "linux:imitante:v0.0.1 (by /u/imitante)"

reddit = praw.Reddit('imitante', user_agent=user_agent)

for submission in reddit.subreddit('learnpython').hot(limit=10):
    print(submission.title)