from dataclasses import dataclass

@dataclass
class MovieCell:
    title: str
    director: str
    rating: int
    im_path: str