#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    """Prints a sorted count of given keywords in the titles of hot articles for a given subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'CustomClient/1.0'}
    params = {'after': after, 'limit': 100}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code != 200:
        return
    
    data = response.json().get('data', {})
    children = data.get('children', [])
    
    if not children:
        return
    
    for post in children:
        title = post['data'].get('title', '').lower()
        for word in word_list:
            word_lower = word.lower()
            if word_lower in title.split():
                word_count[word_lower] = word_count.get(word_lower, 0) + title.split().count(word_lower)
    
    after = data.get('after')
    if after:
        count_words(subreddit, word_list, after, word_count)
    else:
        sorted_word_count = sorted(word_count.items(), key=lambda kv: (-kv[1], kv[0]))
        for word, count in sorted_word_count:
            if count > 0:
                print(f"{word}: {count}")

# Example usage
count_words('python', ['python', 'javascript', 'java'])

