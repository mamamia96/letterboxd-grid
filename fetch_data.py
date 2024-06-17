"""
eventually API calls will be in place here to extract data
"""

from examples import data
from bs4 import BeautifulSoup
import requests
import web_thread
from movie_data import MovieData


#('Challengers', 'Luca Guadagnino', 'images/842301-challengers-0-1000-0-1500-crop.jpg', 4),

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

    # for r in results:
    #     soup = BeautifulSoup(r,'html5lib')

    #     div_tag = soup.find('a', attrs={'data-js-trigger':'postermodal'})
    #     print(div_tag['href'])
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