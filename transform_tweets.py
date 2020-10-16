import json


def main():
    with open("tweets.jsonl", "r+", encoding="utf-8") as input_file, open("tweets_processed.jsonl", "a+",
                                                                          encoding="utf-8") as output_file:
        for line in input_file.readlines():
            # Only write out full tweet, language in metadata
            output = {}
            tweet = json.loads(line)
            output['text'] = tweet['text'] if not tweet['truncated'] else tweet['extended_tweet']['full_text']
            output['meta'] = {"language": tweet['lang'], "id_str": tweet['id_str']}

            json.dump(output, output_file, ensure_ascii=False)
            output_file.write("\n")


if __name__ == '__main__':
    main()
