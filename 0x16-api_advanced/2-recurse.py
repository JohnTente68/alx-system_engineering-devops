#!/usr/bin/python3
import requests

def recurse(subreddit, hot_list=[], after=None):
    """Returns a list of titles of all hot articles for a given subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'CustomClient/1.0'}
    params = {'after': after, 'limit': 100}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code != 200:
        return None
    
    data = response.json().get('data', {})
    children = data.get('children', [])
    
    if not children:
        return None
    
    for post in children:
        hot_list.append(post['data'].get('title'))
    
    after = data.get('after')
    if after:
        return recurse(subreddit, hot_list, after)
    else:
        return hot_list

# Example usage
titles = recurse('python')
if titles:
    for title in titles:
        print(title)
else:
    print(None)

