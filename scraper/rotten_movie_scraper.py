# This script scrapes data from movie pages in Rotten Tomatoes website
# You need a movie_urls.json file to use this. Run rotten_url_scraper.py to get one.

from bs4 import BeautifulSoup
from selenium import webdriver
import json
from datetime import datetime

# Scrape data from a given movie page
def scrape_movie(soup):
    scraped_data = {}

    #Tomatometer
    try:
        tomatometer_text = soup.find('span', {'class': 'mop-ratings-wrap__percentage'}).text.strip()
        scraped_data['tomatometer'] = int(tomatometer_text.replace('%',''))
    except Exception as e:       
        print(str(e))

    #Audience Score
    try:
        score_text = soup.find('span', {'class': 'mop-ratings-wrap__percentage--audience'}).text.replace('liked it','').strip()
        scraped_data['audience_score'] = int(score_text.replace('%',''))
    except Exception as e:
        print(str(e))

        movie_info = soup.find('ul', {'class': 'content-meta info'})
        movie_info_list = movie_info.findAll('div')
        for index, info in enumerate(movie_info_list):
            #Age Rating
            if 'Rating' in str(info):
                try:
                    scraped_data['rating'] = movie_info_list[index+1].text.split(' ')[0]
                except Exception as e:
                    print(str(e))

            #Genres
            elif 'Genre' in str(info):
                try:
                    genres = movie_info_list[index+1].text.split(',')
                    scraped_data['n_genres'] = len(genres)
                    scraped_data['genres'] = []
                    for genre in genres:
                        scraped_data['genres'].append(genre.strip())
                except Exception as e:
                    print(str(e))
            
            #Directors
            elif 'Directed By' in str(info):
                try:
                    directors = movie_info_list[index+1].text.split(',')
                    scraped_data['n_directors'] = len(directors)
                    scraped_data['directors'] = []
                    for director in directors:
                        scraped_data['directors'].append(director.strip())
                except Exception as e:
                    print(str(e))
            
            #Writers
            elif 'Written By' in str(info):
                try:
                    writers = movie_info_list[index+1].text.split(',')
                    scraped_data['n_writers'] = len(writers)
                    scraped_data['writers'] = []
                    for writer in writers:
                        scraped_data['writers'].append(str(writer.strip()))
                except Exception as e:
                    print(str(e))
            
            #Theater Release Date            
            elif 'In Theaters' in str(info):
                try:
                    theater_date_text = movie_info_list[index+1].text.strip().split("\n")[0]
                    scraped_data['theater_release_date'] = datetime.strptime(theater_date_text, '%b %d, %Y').strftime('%m/%d/%y')
                except Exception as e:
                    print(str(e))

            #Disc/Streaming Release Date
            elif 'On Disc' in str(info):
                try:
                    disc_date_text = movie_info_list[index+1].text.strip().split("\n")[0]
                    scraped_data['disc_release_date'] = datetime.strptime(disc_date_text, '%b %d, %Y').strftime('%m/%d/%y')
                except Exception as e:
                    print(str(e))
            
            #Runtime
            if 'Runtime:' in str(info):
                try:
                    scraped_data['runtime'] = int(movie_info_list[index+1].text.strip().replace(' minutes',''))
                except Exception as e:
                    print(str(e))
            
            #Studio
            if 'Studio:' in str(info):
                try:
                    scraped_data['studio'] = str(movie_info_list[index+1].text.strip())
                except Exception as e:
                    print(str(e))
                
        #Cast
        try:
            cast_info = soup.find('div', { 'class' : 'castSection'})
            cast_list = cast_info.findAll('div')
            del cast_list[1::2] # delete duplicates
            scraped_data['cast'] = []
            for actor in cast_list:
                scraped_data['cast'].append(actor.text.strip().split('\n')[0])
        except Exception as e:
            print(str(e))
                
        return scraped_data

# Main   
#Open browser
driver = webdriver.Firefox()

#Get movie URLs from file
with open('movie_urls.json') as movie_urls_file:
    movie_urls = json.load(movie_urls_file)

movie_data = {}    
for title in movie_urls:
    # Get movie's URL
    movie_url = movie_urls[str(title)]

    # Get movie's page source code
    driver.get(movie_url)
    source = driver.page_source
    bsoup = BeautifulSoup(source, 'lxml')
    
    # Scrape movie data
    movie_data[str(title)] = scrape_movie(bsoup)

# Quit web driver
# Comment if you want to keep browser open
# driver.quit()

#Save
now_str = datetime.now().strftime('%m%d%y%H%M%S')
with open('movie_data_' + now_str + '.json', 'w') as movie_data_file:
    json.dump(movie_data, movie_data_file, indent=4)

print("Scraping completed!")
