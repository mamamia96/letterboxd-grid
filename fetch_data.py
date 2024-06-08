"""
eventually API calls will be in place here to extract data
"""

from os import getcwd, listdir
from examples import data

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