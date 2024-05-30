
import tweepy
import subprocess
import pandas as pd 
import os

### Import keys
from x_api_keys import *
from tweet_scrape import *
### Very important ACII art
from aisharpton_ascii import *

### Text generation pre-ample
pre_amble = "As a comedic, but respectful parody version of Reverend Al Sharpton, write a response tweet with a maximum of 280 characters. You should only return the text for the response with no notes or extra characters. The message you are responding to is: "

# Tweepy setup
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_tweet_from_db():  
    df = pd.read_json('data.txt', lines=True)
    # Filter only tweets with more than 15 replies so we don't reply to just anything...
    df = df[df['replyCount'] > 15]  
    # select random row from remaining dataframe
    random_row = df.sample(n=1).iloc[0]
    # Place tweet ID and text in to dictionary
    tweet_dict = {random_row['conversationId']: random_row['rawContent']}
    return tweet_dict

def generate_reply():
    tweet_dict = get_tweet_from_db()
    tweet_id = list(tweet_dict.keys())[0]
    tweet_text = list(tweet_dict.values())[0]
    print(f"Selected Tweet text: {tweet_text}\n")
    query = f"{pre_amble} {tweet_text}"
    result = subprocess.run(['llm', query], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running llm command: {result.stderr}")
        return None
    reply_text = result.stdout.strip()
    return tweet_id, reply_text

def send_tweet(tweet_text):
    print(f"Attempting to send Tweet with text: {tweet_text} ...")
    client.create_tweet(text=tweet_text)

def send_reply(reply_text, reply_to_id):
    print(f"Attempting to reply to tweet {reply_to_id}...")
    try:
        client.create_tweet(text=reply_text, in_reply_to_tweet_id=reply_to_id)
        print('Success! One tweet closer to a dead internet!')
    except Exception as e:
        print(f"error sending tweet: {e}")

def remove_identifier_details(s):
    # Sometimes the LLM returns odd section identifiers. let's clean those up:
    symbols = ['>', '<', '|'] 
    position = min([s.find(symbol) for symbol in symbols if s.find(symbol) != -1], default=len(s))
    return s[:position]

def main():
    while True:
        print(ascii)
        print("""
        SELECT AN ACTION FROM THE BELOW OPTIONS:
        1. Print Information Page
        2. Refresh Tweet Database
        3. Randomly Select and Reply To Tweet from Database
        4. Exit 

        """)
        user_selection = int(input("Enter Selection: "))
        os.system("clear")

        if user_selection == 1:
            print(program_info)
        elif user_selection == 2:
            clear_tweets()
            scrape_tweets()
            os.system("clear")
        elif user_selection == 3:
            print('Generating response... Be patient, this might take little while if no GPU support is present.')
            print('')
            tweet_id, reply = generate_reply()
            #convert tweet ID to int
            tweet_id = int(tweet_id)
            reply = remove_identifier_details(reply)
            # remove quotations from reply if LLM has generated them
            reply.replace('"','')
            print(f"Generated response: {reply}")
            print('')
            send_reply(reply, tweet_id)
        elif user_selection == 4:
            exit()
        else:
            print('INCORRECT INPUT!')

    
if __name__ == "__main__":
    main()






