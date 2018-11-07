import selenium
import time
import sys
import random
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

MAX_HANDLE_ATTEMPTS = 25  # Maximum number of handles scraper will check per run
MINIMUM_FOLLOWER_COUNT = 10000  # Minimum number of followers for bot to consider saving

assert os.environ.get('IG_USERNAME') != None, 'IG_USERNAME not set'
assert os.environ.get('IG_PASSWORD') != None, 'IG_PASSWORD not set'


def get_tags():
    tags = []
    with open('./tags', 'r') as f:
        for line in f:
            tags.append(line.strip())

    return tags


def get_influencers():
    influencers = []
    with open('./influencers', 'r') as f:
        for line in f:
            d = {
                'handle': line.split(',')[0].strip(),
                'name': line.split(',')[1].strip()
            }
            influencers.append(d)

    return influencers


def save_influencer(handle, name):
    influencers = get_influencers()
    name = name.replace(',', ' ')  # Commas sanitized from names
    name = name.encode('ascii', 'ignore').decode('ascii').strip()  # Remove special characters like emojis
    if any(handle == influencer['handle'] for influencer in influencers):
        print('  -> Already saved this influencer before [{}]'.format(handle))
        return

    with open('./influencers', 'a') as f:
        f.write('{},{}\n'.format(handle, name))

    print('  -> Successfully saved <{}, {}>'.format(handle, name))


def parse_follower_count(text):
    text = text.replace(' followers', '')
    text = text.replace(',', '')
    text = text.replace('.', '')

    if 'k' in text:
        text = int(text.replace('k', '')) * 100
    else:
        text = int(text)

    return text


def scrape():
    try:
        tags = get_tags()
        handle_attempts = 0

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(r'./chromedriver', chrome_options=chrome_options)

        # Login
        driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

        time.sleep(3)
        e = WebDriverWait(driver, 3).until(
            lambda driver: driver.find_element_by_xpath("//input[@name='username']"))
        e.send_keys(os.environ.get('IG_USERNAME'))

        e = WebDriverWait(driver, 3).until(
            lambda driver: driver.find_element_by_xpath("//input[@name='password']"))
        e.send_keys(os.environ.get('IG_PASSWORD'))

        e = WebDriverWait(driver, 3).until(
            lambda driver: driver.find_element_by_xpath("//button[contains(.,'Log in')]"))
        time.sleep(3)
        e.send_keys(selenium.webdriver.common.keys.Keys.SPACE)

        # Scrape by tags
        for tag in tags:
            print('Scraping by tag "{}"'.format(tag))
            posts = []
            driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag))

            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                if '/p/' in elem.get_attribute("href"):
                    posts.append(elem.get_attribute("href"))

            print('Found {} posts'.format(len(posts)))

            for post in posts:
                try:
                    name = ''
                    handle_attempts += 1
                    driver.get(post)
                    elems = driver.find_elements_by_xpath("//a[@title]")
                    handle = elems[0].get_attribute("title")

                    print('Inspecting handle {}'.format(handle))
                    driver.get('https://www.instagram.com/{}/'.format(handle))

                    # Scrape name
                    try:
                        elems = driver.find_elements_by_xpath("//h1")
                        name = elems[1].text
                    except Exception:
                        print('No name found.')

                    # Scrape follower count
                    try:
                        elems = driver.find_elements_by_partial_link_text('followers')
                        if parse_follower_count(elems[0].text) < MINIMUM_FOLLOWER_COUNT:
                            print('  -> Not enough followers [{}]'.format(elems[0].text))
                            continue
                    except Exception:
                        print('No follower count found.')

                    save_influencer(handle, name)

                    if handle_attempts > MAX_HANDLE_ATTEMPTS:
                        sys.exit('Max attempts reached')

                    time.sleep(random.choice(range(1, 5)))
                except Exception as e:
                    print(e)


    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == '__main__':
    scrape()
