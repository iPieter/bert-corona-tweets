import json


def main():
    with open("../data/tweets_sample_03_nov_2020.jsonl", "r+", encoding="utf-8") as input_file, open(
            "../data/tweets_processed.jsonl", "a+",
            encoding="utf-8") as output_file:
        for line in input_file.readlines():
            # Only write out full tweet, language in metadata
            output = {}
            tweet = json.loads(line)
            output['text'] = tweet['text'] if not tweet['truncated'] else tweet['extended_tweet']['full_text']
            if 'retweeted_status' in tweet:
                output['text'] = 'Context:\n' + \
                                 (tweet['retweeted_status']['text'] if not tweet['retweeted_status']['truncated'] else
                                  tweet['retweeted_status']['extended_tweet'][
                                      'full_text']) + '\n----------\n' + 'Tweet:\n' + \
                                 output['text']
            output['meta'] = {"language": tweet['lang'], "id_str": tweet['id_str']}

            json.dump(output, output_file, ensure_ascii=False)
            output_file.write("\n")


def generate_stats():
    with open("../data/tweets_remote.jsonl", "r+", encoding="utf-8") as input_file, open("../data/tweets.csv", "a+",
                                                                                         encoding="utf-8") as output_file:
        for line in input_file.readlines():
            # Only write out full tweet, language in metadata
            output = {}
            tweet = json.loads(line)
            output_file.write("{},{}\n".format(tweet['created_at'], tweet['lang']))


if __name__ == '__main__':
    main()
