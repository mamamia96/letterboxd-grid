"""
eventually API calls will be in place here to extract data
"""

from examples import data
from bs4 import BeautifulSoup
import requests
import web_thread
from movie_data import MovieData
from datetime import datetime
import re
import urllib.parse
#('Challengers', 'Luca Guadagnino', 'images/842301-challengers-0-1000-0-1500-crop.jpg', 4),

def scrape2(user: str, month: int) -> list:

    # maybe we split this up into two funcs

    url = f'https://letterboxd.com/{user}/rss/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'xml')

    items = soup.find_all('item')



    def is_movie(item) -> bool:
        return  str(item.find('link')).find(f'https://letterboxd.com/{user}/list/') == -1 

    def watched_this_month(item) -> bool:
        return get_watched_date(item).month == month

    def get_watched_date(item) -> datetime:
        date_split = re.split(pattern='<|>', string=str(item.find("letterboxd:watchedDate")))[2].split('-')
        date = datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]))
        return date
    
    def get_movie_title(item) -> str:
        return re.split(pattern='<|>', string=str(item.find("letterboxd:filmTitle")))[2]

    def get_movie_rating(item) -> int:
        rating_tag = item.find("letterboxd:memberRating")
        if not rating_tag: return -1
        return float(re.split(pattern='<|>', string=str(rating_tag))[2])

    def get_poster_url(item) -> str:
        # attrs are broken inside description tag so we have to do this a little more manually
        url_slice = [m.start() for m in re.finditer('"', str(item.find('description')))]
        return str(item.find('description'))[url_slice[0]:url_slice[1]]

    # sorting movies by date
    items = sorted(filter(is_movie, items), key=lambda x: get_watched_date(x), reverse=True)
    # getting movies watched this month
    items = list(filter(watched_this_month, items))

    # reverse these? ^^
    
    movie_titles = list(map(get_movie_title, items))
    movie_ratings = list(map(get_movie_rating, items))
    movie_poster_urls = list(map(get_poster_url, items))
    # async download posters?

    # new soup to get last [number of movies watched this month] movie links from recently watched page 
    url = f'https://letterboxd.com/{user}/films/by/date/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html5lib')

    movie_links = []

    for i, table in enumerate(soup.find_all('li', attrs={'class':'poster-container'})):

        if i == len(movie_titles): break
        # movie titles
        movie_links.append(table.find('div')['data-film-slug'])

    for e in zip(movie_titles, movie_links):
        print(e)

    return
    # put selenium data retrieval into threads because they need to wait for js on page to load
    threads = [None for _ in range(len(movie_titles))]
    wthread_containers = []

    for i, title in enumerate(movie_titles):

        print(title)
        break

        wthread_containers.append(web_thread.WebThreadContainer(f'https://letterboxd.com/film/{movie_data.title}/'))
        threads[i] = wthread_containers[i]._get_html_with_js()
        threads[i].start()

    for thread in threads:
        thread.join()

    # map poster_url and director to lists now

    def get_poster_url(wthread_container: web_thread.WebThreadContainer) -> str:
        soup = BeautifulSoup(cl.html, 'html5lib')
        return soup.find('a', attrs={'data-js-trigger':'postermodal'})['href']

    def get_director(wthread_container: web_thread.WebThreadContainer) -> str:
        soup = BeautifulSoup(cl.html, 'html5lib')
        return soup.find('a', attrs={'class':'contributor'})['href']

    movie_poster_urls = list(map(get_poster_url, wthread_containers))
    movie_directors = list(map(get_director, wthread_containers)) 


    for mv in zip(movie_titles, movie_directors, movie_ratings, movie_poster_urls):
        print(mv)

def scrape(user: str) -> list:

    # list of data
    movie_data_collection = []

    url = f'https://letterboxd.com/{user}/films/by/date/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html5lib')

    movie_titles = []

    for i, table in enumerate(soup.find_all('li', attrs={'class':'poster-container'})):


        # movie titles
        movie_titles.append(table.find('div')['data-film-slug'])

        # rating -1 if movie is unrated
        poster_tag = table.find('p', attrs={'class':'poster-viewingdata'})
        rating = -1
        if str(poster_tag).find('rating') != -1:
            rating = str(poster_tag).count('★')
            rating += (str(poster_tag).count('½') * 0.5)
        #print(f'{movie_titles[i]} - {rating}')

        # storing in dataclass
        movie_data_collection.append(MovieData(table.find('div')['data-film-slug'], rating))

        if i == 10: break

    # put selenium data retrieval into threads because they need to wait for js on page to load
    threads = [None for _ in range(len(movie_titles))]
    wthread_containers = []

    for i, movie_data in enumerate(movie_data_collection):
        wthread_containers.append(web_thread.WebThreadContainer(f'https://letterboxd.com/film/{movie_data.title}/'))
        threads[i] = wthread_containers[i]._get_html_with_js()
        threads[i].start()
        # print(f'starting THREAD - {movie_data.title}')

    for thread in threads:
        thread.join()

    for i, cl in enumerate(wthread_containers):
        soup = BeautifulSoup(cl.html, 'html5lib')
        # print(soup.prettify())
        div_tag = soup.find('a', attrs={'data-js-trigger':'postermodal'})
        #print(div_tag['href'])

        movie_data_collection[i].poster_url = div_tag['href']

        # <a class="contributor" href="/director/don-hertzfeldt/">
        director_tag = soup.find('a', attrs={'class':'contributor'})
        # print(director_tag['href'])
        movie_data_collection[i].director = director_tag['href']

    return
    for movie_data in movie_data_collection:
        print(repr(movie_data))

def get_data(number_of_movies: int) -> list:

    # because I don't want to manually fill out dataset we are just choosing
    # number_of_movies options from our small dataset in examples.py

    # image_paths = listdir(f'{getcwd()}/images') might need this later
    
    ret_data = []
    movie_ind = 0
    for i in range(number_of_movies):
        ret_data.append(data[movie_ind])
        movie_ind += 1
        if movie_ind >= len(data):
            movie_ind = 0

    return ret_data