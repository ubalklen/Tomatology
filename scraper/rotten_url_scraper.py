from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from datetime import datetime

# Set up URLs
base_url = 'https://www.rottentomatoes.com'
all_movie_url = base_url + '/browse/dvd-streaming-all'

# Set up web driver
driver = webdriver.Firefox()
driver.get(all_movie_url)

# Click "Show More" button to expand all the movies
show_more_button = driver.find_element_by_xpath('//*[@id="show-more-btn"]/button')
print('Clicking the button to expand all the movies...')
while(True):
    try:
        show_more_button.click()
        time.sleep(1)
    except Exception as e:
        print(str(e))
        print('Cannot click anymore. Moving on...')
        break

# Scrape URLs
print('Scraping the URLs...')
soup = BeautifulSoup(driver.page_source,"lxml")
movies = soup.find('div', {'class' :"mb-movies"})
movie_list = {}
for movie in movies:
    movie_url = movie.find('a')
    if movie_url is not None:
        movie_url = base_url + movie_url['href']
        title = movie.find('h3',{'class' : "movieTitle"}).text
        movie_list[title] = movie_url

# Quit web driver
# Comment if you want to keep browser open
# driver.quit()

# Save and finish
now_str = datetime.now().strftime('%m%d%y%H%M%S')
print('Saving movie_urls_' + now_str + '.json')
with open('movie_urls_' + now_str + '.json', 'w') as file:
    json.dump(movie_list,file, indent=4)

print('URL scraping completed!')
