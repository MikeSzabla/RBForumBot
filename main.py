import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def main():
    # login to forum -> verify that logged in -> create link list -> go through list one-by-one (check against cache)
    browser = webdriver.Chrome()
    browser.maximize_window()
    login(browser)
    links = get_links(browser, 10)

    username = browser.find_element_by_id('current-user').find_element_by_class_name('icon').get_attribute('href')[30:]

    #links = filter_list(links, username)
    for link in links:
        read(browser, link)
        cache(link, username)
    browser.quit()


# open log in page, wait until logged in
def login(browser):
    browser.get('https://www.roblox.com/login?returnUrl=https://apis.roblox.com/application-authorization/v1/authorize%3Fclient_id%3De7eec6fe-31bd-4b83-be99-f1fd2cabfafb%26scope%3Dopenid+profile+email%26response_type%3Dcode%26redirect_uri%3Dhttps%3A%2F%2Fdevforum.roblox.com%2Fauth%2Foidc%2Fcallback%26state%3De4ea1dc7803b0de76393db5459c7113ef0742abaaa5d04db%26nonce%3D5a637872caf2a748de3aa633be8297232ef0bad3c639d1c09778a4d17259d42a')
    print("Log In.")
    b = input('After logging in, type anything and enter to continue: ')


def get_links(browser, max_scroll):
    scroll_pause_time = 3
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


def filter_list(links, username):  # takes in a list of links, uses cache to make sure there are no duplicates
    filtered_list = links
    # TODO: read in cache, compare against links, return link entries with no match
    return filtered_list


def read(browser, link):
    browser.get(link)
    like_button = browser.find_element_by_class_name('header-buttons')


def cache(link, username):
    with open('cache.json') as f:
        data = json.load(f)
    users = data['users']
    current_user = {'username': '', 'used-links': []}
    for user in users:
        if user['username'] == username:
            print('found him')


def test():
    with open('cache.json') as f:
        data = json.load(f)
    users = data['users']
    current_user = {'username': '', 'used-links': []}
    for user in users:
        if user['username'] == 'xxbladeartxx':
            print('found him')


# main()
test()
