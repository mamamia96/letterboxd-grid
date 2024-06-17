from dataclasses import dataclass

@dataclass
class MovieData:
    title: str
    rating: int 
    director: str = ''
    poster_url: str = ''

    def __repr__(self) -> str:
        return f'''=={self.title}==

by: {self.director}
rating: {self.rating}/5
poster_url: {self.poster_url}
        '''


# ('Challengers', 'Luca Guadagnino', 'images/842301-challengers-0-1000-0-1500-crop.jpg', 4),