import praw
import re
import argparse
import datetime
import os
from markov import Markov

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddit", type=str, default="all", help="choose the subreddit (default=all)")
    parser.add_argument("-p", "--posts", type=int, default="1000", help="How many posts to read (default=10000)")
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

def fileHeader(date):
    return """---
https://github.com/LuisSousaRego/imitante
Subreddit: {}
Posts used: {}
Titles used: {}
Time: {}
Markov-chain order: {}
---

""".format(args.subreddit, postCounter, titleCounter, date.strftime("%Y/%m/%d %H:%M:%S"), args.order)
    


#
# Start
#

args = getArgs()
postCounter = 0
titleCounter = 0

subreddit = getSubreddit(args.subreddit)
mkSelfPosts = Markov()
mkTitles = Markov()


for submission in subreddit.search('self:yes', sort='relevance', time_filter='all', limit=args.posts):
    # title
    titleList = submission.title.split(" ")
    if len(titleList) >= 2: # skip titles that are too small
        mkTitles.addFirstWord(tuple(titleList[0]))
        for t in range(1, len(titleList)):
            mkSelfPosts.addWordTransition(tuple(titleList[t - 1]), titleList[t])
        titleCounter += 1

    # post
    processedText = cleanText(submission.selftext)
    words = re.findall(r'\S+|\n', processedText)
    if len(words) >= args.order + 1: # skip posts that are too small
        firstWords = [ words[o] for o in range(args.order) ]
        mkSelfPosts.addFirstWord(tuple(firstWords))

        for i in range(args.order, len(words)):
            previousWords = [words[x] for x in range(i - args.order, i)]
            mkSelfPosts.addWordTransition(tuple(previousWords), words[i])
            #if i == len(words) - 1:
                #mkSelfPosts.addWordTransition(words[i], " ") # can't remember why this is here
        postCounter += 1

generatedTitle = mkTitles.generateText()
generatedText = mkSelfPosts.generateText()


nowTime = datetime.datetime.now()
filename = "../text/{}-{}.txt".format(nowTime.strftime("%Y%m%d%H%M%S"), args.subreddit)
os.makedirs(os.path.dirname(filename), exist_ok=True)
f = open(filename, "w")
f.write(fileHeader(nowTime) + "-" + generatedTitle + "-\n" + generatedText)

print("Output in file: {}".format(filename[8:]))