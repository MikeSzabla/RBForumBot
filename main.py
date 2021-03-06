import time
import json
from selenium import webdriver
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class User:
    def __init__(self, username, used_links, index, last_y_offset):
        self.username = username
        self.used_links = used_links
        self.index = index
        self.last_y_offset = last_y_offset

    def print_info(self):
        print('Username: {} Index in file: {}'.format(self.username, self.index))

    def get_dict(self):
        return {"username": self.username, "used_links": self.used_links}


def main():
    # login to forum -> verify that logged in -> create link list -> go through list one-by-one (check against cache)
    browser = webdriver.Chrome()
    browser.maximize_window()
    login(browser)
    links = get_links(browser, 10)

    username = browser.find_element_by_id('current-user').find_element_by_class_name('icon').get_attribute('href')[30:]
    current_user = init_user(username)

    #links = filter_list(links, current_user)

    for link in links:
        read(browser, link)
        cache(link, current_user)

    browser.quit()


# open log in page, wait until logged in
def login(browser):
    # TODO: This is hella scuffed rn. Add a check to make sure the user is logged in and on a valid page
    browser.get('https://www.roblox.com/login?returnUrl=https://apis.roblox.com/application-authorization/v1/authorize%3Fclient_id%3De7eec6fe-31bd-4b83-be99-f1fd2cabfafb%26scope%3Dopenid+profile+email%26response_type%3Dcode%26redirect_uri%3Dhttps%3A%2F%2Fdevforum.roblox.com%2Fauth%2Foidc%2Fcallback%26state%3De4ea1dc7803b0de76393db5459c7113ef0742abaaa5d04db%26nonce%3D5a637872caf2a748de3aa633be8297232ef0bad3c639d1c09778a4d17259d42a')
    print("Log In.")
    b = input('After logging in, type anything and enter to continue: ')


# get_links: returns a list of forum links retrieved from a table on the forum.
# Takes in a browser driver object and a value max_scroll, which determines a max amount of screen lengths to
# scroll down on the infinite page.
def get_links(browser, max_scroll):
    scroll_pause_time = 1
    i = 1
    # finds the initial bottom value of the page and the current Y-Offset of the page
    bottom = browser.execute_script("return document.body.scrollHeight;")
    current_pos = browser.execute_script("return window.pageYOffset") + browser.execute_script(
        'return document.documentElement.clientHeight')
    while True:
        # uses difference in bottom and current_pos to scroll
        browser.execute_script("window.scrollBy(0, {})".format(bottom-current_pos))
        i += 1
        time.sleep(scroll_pause_time)

        # updates bottom and current_pos to new values
        bottom = browser.execute_script("return document.body.scrollHeight;")
        current_pos = browser.execute_script("return window.pageYOffset") + browser.execute_script(
            'return document.documentElement.clientHeight')

        # Breaks if bottom is reached or max amount of scrolls is exceeded
        print('i is {} current_pos is {} bottom is {}'.format(i, current_pos, bottom))
        if current_pos == bottom:
            print('broken because end of page')
            break
        if i > max_scroll:
            print('broken because limit reached')
            break

    links = []
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table = soup.find('table', class_='topic-list ember-view')
    for post in table.find_all('tbody'):
        all_a = post.find_all('a', class_='title raw-link raw-topic-link', href=True)
        for a in all_a:
            links.append('https://devforum.roblox.com'+a['href'])

    return links


def filter_list(links, current_user):  # takes in a list of links, uses cache to make sure there are no duplicates
    # TODO: read in cache, compare against links, return link entries with no match
    filtered_list = links
    current_list = current_user.used_links

    return filtered_list


def read(browser, link):  # used the browser and given link to open the page and slowly scroll through to bottom
    browser.get(link)

    scroll_pause_time = 1
    i = 1
    # finds the initial bottom value of the page and the current Y-Offset of the page
    bottom = browser.execute_script("return document.body.scrollHeight;")
    current_pos = browser.execute_script("return window.pageYOffset") + browser.execute_script(
        'return document.documentElement.clientHeight')
    while True:
        # uses difference in bottom and current_pos to scroll
        browser.execute_script("window.scrollBy(0, {})".format(bottom-current_pos))
        i += 1
        time.sleep(scroll_pause_time)

        # updates bottom and current_pos to new values
        bottom = browser.execute_script("return document.body.scrollHeight;")
        current_pos = browser.execute_script("return window.pageYOffset") + browser.execute_script(
            'return document.documentElement.clientHeight')

        # Breaks if bottom is reached or max amount of scrolls is exceeded
        print('i is {} current_pos is {} bottom is {}'.format(i, current_pos, bottom))
        if current_pos == bottom:
            print('broken because end of page')
            break

    like_button = browser.find_element_by_class_name('header-buttons')


def init_user(username):  # initialized the current_user object and updates the cache if necessary
    with open('cache.json') as f:
        data = json.load(f)
    users = data['users']

    found = False
    index = 0
    for entry in users:
        if entry['username'] == username:
            current_user = User(username, entry['used-links'], index)
            found = True
            break
        else:
            index += 1

    if not found:
        current_user = User(username, [], index)
        user_dict = current_user.get_dict()
        users.append(user_dict)
        with open('cache.json', 'w') as f:
            json.dump(data, f, indent=2)

    return current_user


def cache(link, current_user):
    with open('cache.json') as f:
        data = json.load(f)
    users = data['users']

    # potential issue: will the current_user's used_link list be consistent outside of the function?
    current_user.used_links.append(link)
    users[current_user.index] = current_user.get_dict
    with open('cache.json', 'w') as f:
        json.dump(data, f, indent=2)


def test(given_user):
    pass

# main()
test_user = init_user('newname')
test_user.print_info()


