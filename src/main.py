import praw
import re
from markov import Markov

def getPortugal():
    user_agent = "linux:imitante:v0.0.1 (by /u/imitante)"
    reddit = praw.Reddit('imitante', user_agent=user_agent)
    return reddit.subreddit('portugal')

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
    regexChars = r'\**\(*\)*~*(&#x200B)*'
    result = re.sub(regexChars, '', result)
    
    return result


portugal = getPortugal()
mk = Markov()

for submission in portugal.hot(limit=10000):
    if submission.is_self:
        processedText = cleanText(submission.selftext)
        words = re.findall(r'\S+|\n', processedText)
        if len(words) < 1:
            continue
        mk.addFirstWord(words[0])

        for i in range(1, len(words)):
            mk.addWordTransition(words[i - 1], words[i])
            if i == len(words) - 1:
                mk.addWordTransition(words[i], " ")
        mk.postCounter += 1

print(mk.generateText())
