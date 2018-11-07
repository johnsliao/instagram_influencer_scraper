# Instagram Influencer Scraper

## What is this
This script scrapes `handle` and `name` from top posts on Instagram based on #hashtags using selenium webdriver

### How it works
1. Logs in
2. Find instagram top posts by provided #hashtag
3. Navigate to each `@handle` and saves `@handle`, `name` in a file

## Set up
- Python 3.x+
- `pip`

1. `pip install -r requirements.txt`
2. Download [chromedriver](http://chromedriver.chromium.org/). Place in root directory.
3. Create `influencers` and `tags` file (no extension) in root directory
4. Set `IG_USERNAME` and `IG_PASSWORD` environment variables
5. `$ python app.py`

`tags` file should look like:
```
gaming
mensfashion
```
 
Results will be stored in `influencers` file. E.g.
```
pewdiepie,PewDiePie
markiplier,Markiplier
```
## Configuration
1. `MAX_HANDLE_ATTEMPTS` is set in `app.py` to `25` by default. Sets the number of posts the script will scrape in a single run.  
2. `MINIMUM_FOLLOWER_COUNT` is set to `10000` by default. Sets the minimum number of followers for influencer to be recorded.

## Features
- Duplicate `@handle`s will not be saved to `influencers` file

## Please note
- Emojis/special characters in names are ignored when saving to `influencers`
- Commas in names are replaced as a space
