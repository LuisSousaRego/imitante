import praw
import re
import argparse
import datetime
from markov import Markov

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddit", type=str, default="all", help="choose the subreddit (default=all)")
    parser.add_argument("-p", "--posts", type=int, default="10000", help="How many posts to read (default=10000)")
    parser.add_argument("-o", "--order", type=int, default="1", help="order of the markov chain (default=1)")

    return parser.parse_args()


def getSubreddit(subreddit):
    user_agent = "linux:imitante:v0.1.0 (by /u/imitante)"
    reddit = praw.Reddit('imitante', user_agent=user_agent)
    return reddit.subreddit(subreddit)

def cleanText(text):
    result = ""
    # remove Links Format
    regexLinksFormat = r"\[(.+)]\(http.+\)"
    subst = "\\1"
    result = re.sub(regexLinksFormat, subst, text, 0, re.IGNORECASE)

    # remove other links
    regexOtherLinks = r'http\S+'
    result = re.sub(regexOtherLinks, '', result)

    # remove unwanted chars
    regexChars = r'\**\(*\)*~*(&#x200B;?)*'
    result = re.sub(regexChars, '', result)
    
    return result



args = getArgs()
postCounter = 0

subreddit = getSubreddit(args.subreddit)
mkSelfPosts = Markov()

for submission in subreddit.hot(limit=args.posts):
    if submission.is_self:
        processedText = cleanText(submission.selftext)
        words = re.findall(r'\S+|\n', processedText)
        if len(words) < args.order + 1: # skip posts that are too small
            continue
        
        firstWords = [ words[o] for o in range(args.order) ]
        mkSelfPosts.addFirstWord(tuple(firstWords))

        for i in range(args.order, len(words)):
            previousWords = [words[x] for x in range(i - args.order, i)]
            mkSelfPosts.addWordTransition(tuple(previousWords), words[i])
            if i == len(words) - 1:
                mkSelfPosts.addWordTransition(words[i], " ") # can't remember why this is here
        postCounter += 1

today = datetime.datetime.now()
filename = "../text/{}-{}-{}-{}.txt".format(today.strftime("%Y%m%d%H%M%S"), args.subreddit, args.posts, args.order)
f = open(filename, "w")

text = mkSelfPosts.generateText()
f.write(text)