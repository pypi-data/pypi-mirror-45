import urllib.request
from bs4 import BeautifulSoup

twitter_url = 'https://twitter.com/'

def request_url(url):
    # Query the website (url) and return the html
    try:
        page = urllib.request.urlopen(url)
        # Parse the html
        return BeautifulSoup(page, 'html.parser')
    except:
        return 'No response from Twitter.com'

# Get statistics from a given username: (amount of followers, amount of following, amount of tweets)
def stats(user_name, stat):
    response = request_url(twitter_url + user_name)
    requests = ['followers','following','tweets is-active']

    for req in requests:
        if req.split()[0] == stat:
            stat_request = req 

    try:    
        nav_item = response.find(class_='ProfileNav-item ProfileNav-item--' + stat_request)
        if nav_item is not None: 
            return nav_item.find(class_='ProfileNav-value').get_text().strip()
        else:
            return f'User doesnt have any {req.split()[0]}'    
    except:
        return 'User cant be found'

