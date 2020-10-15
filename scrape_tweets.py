import sys
import csv
import tweepy
import json
import re
import time


def get_set_of_places():
    locations = set()
    with open('locations.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            loc = re.sub(r'\s\(.*\)', '', row[1]).lower()
            if len(loc) > 5:  # don't add too short strings (e.g. "As")
                locations.add(loc)

    locations.add("belgique")
    locations.add("belgium")
    locations.add("belgie")
    locations.add("belgië")
    locations.add("🇧🇪")
    return locations


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.locations = get_set_of_places()
        self.api = api

    def estimate_region(self, status):

        user_status = re.sub(r'[,•|\-\(\)]', ' ',
                             status.user.description.lower()).split() if status.user.description else []
        user_location = re.sub(r'[,•|\-\(\)]', ' ',
                               status.user.location.lower()).split() if status.user.location else []

        for location in self.locations:
            if location in user_location:
                print("=> Location estimation ({})".format(location))
                return True
            if location in user_status:
                print("=> Description estimation ({})".format(location))
                return True

        return False

    def on_status(self, status):
        if self.estimate_region(status):
            status.text = status.text if not status.truncated else status.extended_tweet['full_text']
            print(status.text)
            with open("tweets.jsonl", "a+", encoding="utf-8") as file_object:
                # Append 'hello' at the end of file
                json.dump(status._json, file_object, ensure_ascii=False)
                file_object.write("\n")
            print("------")


def main():
    auth = tweepy.OAuthHandler(sys.argv[1], sys.argv[2])
    auth.set_access_token(sys.argv[3], sys.argv[4])

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener(api)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, wait_on_rate_limit=True,
                             wait_on_rate_limit_notify=True)
    locations = [2.427978515625,
                 49.51094351526262,
                 6.39404296875,
                 51.44716034698012]

    myStream.filter(
        track=["coronAlert", "lockdown", "#lockdown", "mondmasker", "#coronavirus", "corona", "virus", "covid",
               "avondklok", "curfew", "Couvre-feu"],
        languages=["nl", "en", "fr"])


if __name__ == '__main__':
    retries = [1, 2, 4, 8, 16]
    while retries:
        try:
            main()
        except ConnectionError as e:
            print("Connection error, retrying")
            print(e)
            time.sleep(retries.pop())
