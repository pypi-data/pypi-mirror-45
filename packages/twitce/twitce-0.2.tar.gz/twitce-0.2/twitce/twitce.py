import urllib.request
from bs4 import BeautifulSoup

twitter_url = 'https://twitter.com/'

def request_url(url, user):
    # Query the website (url) and return the html
    try:
        url += user
        page = urllib.request.urlopen(url)
        # Parse the html
        return BeautifulSoup(page, 'html.parser')

    except:
        return '404'


# Get statistics from an user, requires a username and a stat: 'followers','following','tweets'
def stats(user_name, stat):
    requests = ['followers','following','tweets is-active']

    if user_name == '': return 'First argument must be provided' 
    elif stat == '': return 'Second argument must be provided'

    if stat in requests:
        stat_request = stat
    elif stat == 'tweets':
        stat_request = requests[2]          
    else:
        return f'Does not recognize "{stat}" as one of the enumerations'    

    response = request_url(twitter_url, user_name)

    if response == '404':
        return 'User does not exist'

    nav_item = response.find(class_='ProfileNav-item ProfileNav-item--' + stat_request)

    if nav_item is not None: 
        return nav_item.find(class_='ProfileNav-value').get_text().strip()
    else:
        return f'User doesnt have any {stat}'    


# Get profile information, requires a username and a option: 'name','screenname','bio','location','url','joinDate','birthdate'
def profile(user_name, option):
    requests = ['name','screenname','bio','location','url','joinDate','birthdate']

    if user_name == '': return 'First argument must be provided' 
    elif option == '': return 'Second argument must be provided'

    if option in requests:
        option_request = option
    elif option == 'join':
        option_request = requests[5]
    elif option == 'birth':
        option_request = requests[6]    
    else:   
        return f'Does not recognize "{option}" as one of the enumerations'
    
    response = request_url(twitter_url, user_name)

    if response == '404':
        return 'User does not exist'
        
    profile_item = response.find(class_='ProfileHeaderCard-' + option_request).get_text().strip()

    if profile_item == '': return 'None specified'    
    else: return profile_item    
    