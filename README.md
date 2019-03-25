# imitante

Generate text from subreddits self posts using markov chains

## Prerequisites

- A reddit account and a [reddit script app](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)
- [Python 3](https://www.python.org/)
- [Praw](https://praw.readthedocs.io/en/latest/)
- praw.ini file inside the `/src/` directory


### praw.ini file

Create a [praw.ini file](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html?highlight=praw.ini#praw-ini-files) inside the /src/ directory
Add a new bot to the file with your reddit app credentials

```
[imitante]
client_id=yourclientid
client_secret=yourclientsecret
password=yourpassword
username=yourusername
```


## Get started

Open the terminal in the project folder and run the `main.py` file with:
```
python3 /src/main.py
```
For information on available arguments run:
```
python3 /src/main.py -h
```

The generated text will be written in a .txt file inside `/text/` directory