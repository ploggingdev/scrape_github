import requests
import json
import os
import time

def get_lang_stats():
    access_token = os.environ['github_token']
    with open('github_scraper/all_repos.jsonl') as f:
        with open('lang_data.jsonl','w') as lang_file:
            for line in f:
                lang_url = "{}?access_token={}".format(json.loads(line)['languages_url'], access_token)
                try:
                    response_data = requests.get(lang_url)
                    response_data.raise_for_status()
                except requests.exceptions.HTTPError as ex:
                    print(ex)
                    lang_file.write("{}\n")
                else:
                    lang_file.write("{}\n".format(response_data.text))
                finally:
                    #check if api limit is reached
                    api_limit_check(response_data)
                

def api_limit_check(response_data):
    api_limit = int(response_data.headers['X-RateLimit-Limit'])
    api_calls_remaining = int(response_data.headers['X-RateLimit-Remaining'])
    reset_time = int(response_data.headers['X-RateLimit-Reset'])

    if api_calls_remaining == 0:
        print("Sleeping for {} minutes".format((reset_time - time.time() + 30)/60))
        time.sleep(reset_time - time.time() + 30)
                
    print("Api calls remaining : {}\nMinutes to reset api limit : {}\n".format(api_calls_remaining, (reset_time - time.time())/60))

if __name__ == "__main__":
    get_lang_stats()