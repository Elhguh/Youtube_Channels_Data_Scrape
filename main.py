import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# Set up the driver
driver = webdriver.Chrome()

# Navigate to the YouTube channel
channel_url = 'https://www.youtube.com/@JohnWatsonRooney/videos'
driver.get(channel_url)

# Scroll down to load all the videos
body = driver.find_element(By.TAG_NAME, 'body')
for i in range(30):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# Get the video links
video_links = []
videos = driver.find_elements(By.XPATH, './/a[@id="video-title"]')
for video in videos:
    link = video.get_attribute('href')
    if link not in video_links:
        video_links.append(link)

info = []
# Scrape data from each video
for link in video_links:
    print(f"Processing video: {link}")
    driver.get(link)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract information from the video page
    try:
        title = soup.find('yt-formatted-string', id_='video-title').text.strip()
    except:
        title = 'N/A'
    try:
        views = soup.find('span', class_='inline-metadata-item style-scope ytd-video-meta-block').text.strip()
    except:
        views = 'N/A'
    try:
        posting_time = driver.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text.strip()
    except:
        posting_time = 'N/A'
    try:
        video_duration = soup.find('span', {'class': 'ytp-time-duration'}).text.strip()
    except:
        video_duration = 'N/A'
    try:
        subs = soup.find('span', {'class': 'yt-subscription-button-subscriber-count-branded-horizontal'}).text.strip()
    except:
        subs = 'N/A'

    # Print the data for the current video
    print(f'Title: {title}')
    print(f'Views: {views}')
    print(f'Posting time: {posting_time}')
    print(f'Video duration: {video_duration}')
    print(f'Subs: {subs}')

    info.append([title, views, posting_time, video_duration, subs])

# Quit the driver
driver.quit()

df = pd.DataFrame(info, columns = ['Title', 'Views', 'Posting Time', 'Duration', 'Subscribers'])
df.to_csv(f'DuTupCrepe1.csv')
