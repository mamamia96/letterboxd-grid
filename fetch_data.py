"""
eventually API calls will be in place here to extract data
"""


from os import getcwd, listdir
from examples import data

from bs4 import BeautifulSoup
import requests


def scrape(user: str) -> list:
    url = f'https://letterboxd.com/{user}/films/by/rated-date/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    movie_titles = []

    for i, table in enumerate(soup.find_all('li', attrs={'class':'poster-container'})):
        #print(f'=={i}==\n\n{table}')
        movie_titles.append(table.find('div')['data-film-slug'])
        
        if i == 5: break

    for movie in movie_titles:
        r = requests.get(f'https://letterboxd.com/film/{movie}/')
        soup = BeautifulSoup(r.content, 'html5lib')
        meta_tag = soup.find('meta',attrs={'property':'og:image'})
        print(meta_tag.prettify())
        # div_tag = soup.find('div', {'class':'poster-wrapper'})
        # poster_img = div_tag.find('img')
        # img_url = poster_img['src']
        # print(img_url)

        # print(soup.prettify())
    # print(table.prettify())

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

