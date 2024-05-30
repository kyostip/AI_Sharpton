#! /usr/bin/python3

import subprocess

### Python script utilizing TWScrape (https://github.com/vladkens/twscrape) to find random tweets to reply to.
### for obvious reasons details on the accounts used for scraping will not be included.
### This is very ghetto, but I am not paying a $100/m subscription to twitter API for this exercise...

# These are the key words we will be using to attempt to find tweets
keywords = [
    "Biden",
    "Trump",
    "Election",
    "Supreme Court",
    "Congress",
    "Senate",
    "Democrats",
    "Republicans",
    "Impeachment",
    "Polls",
    "Justice",
    "Political",
    "Government",
    "Policy",
    "President",
    "White House",
    "Constitution",
    "Amendment",
    "Protest",
    "Civil Rights",
    "Healthcare",
    "Economy",
    "Welfare",
    "Social Security",
    "Liberty",
    "Equality",
    "Justice",
    "Human Rights",
]

#remove old data file
def clear_tweets():
    try:
        os.remove('data.txt')
    except FileNotFoundError:
        print("no existing data file was present, no need to remove")
    except Exception as e:
        print("Old data cleared ...")

        # recreate file
    with open('data.txt', 'w') as fp:
        pass


# Iterate through our keywords and scrape for new tweets
def scrape_tweets():
    for word in keywords:
        try:
            print(f'Searching for new tweets for the query: {word} ...')
            command = ['twscrape', 'search', '--limit=10', word]
            result = subprocess.run(command, check=True, text=True, capture_output=True)     
            with open('data.txt', 'a') as file:
                file.write(result.stdout)        
        except subprocess.CalledProcessError as e:
            print(f'Something went wrong and process returned non-zero exit status: {e.returncode}')
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

