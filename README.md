# imitante

Generate text from subreddits self posts using markov chains


## Prerequisites

- A reddit account and a [reddit script app](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)
- [Python 3](https://www.python.org/)
- [Praw](https://praw.readthedocs.io/en/latest/)
- praw.ini file inside the `src/` directory


### praw.ini file

Create a [praw.ini file](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html?highlight=praw.ini#praw-ini-files) inside the /src/ directory
Add a new bot to the file with your reddit app credentials by appending the following to your `praw.ini` file:

```
[imitante]
client_id=yourclientid
client_secret=yourclientsecret
password=yourpassword
username=yourusername
```


## Get started

Open the terminal in the `src/` directory inside the project and run the `main.py` file with:

`python3 main.py`

The generated text will be written in a .txt file inside `text/` directory


## Options

### --subreddit

Choose which subreddit the posts are from

`python3 main.py --subreddit WritingPrompts`


### --posts

Max number of posts to read

`python3 main.py --posts 500`


### --order

Order of the Markov chain

Higher number should get better results, too high and it will just quote text from posts. Recommended 1 to 3

`python3 main.py --order 2`
