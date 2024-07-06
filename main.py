from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import fetch_data
from time import time
from ratio_tester import get_moviecells

resize_factor: float = 0.2
image_gap: int = 10

info_box_width: int = 500
info_box_height: int = 500

def factor_to_ratio(pair: tuple) -> float:
	return pair[0]/pair[1]

def valid_ratio_exists(ratios: list, max_ratio: float, min_ratio: float) -> bool:
	for ratio in ratios:
		if ratio >= min_ratio and ratio <= max_ratio:
			return True
	return False

def get_grid_size(n: int) -> tuple:
	MIN_RATIO = 1
	MAX_RATIO = 2.5

	while True:
		factors = list(map(reorder_pair, get_factors(n)))
		print(factors)
		factor_ratios = list(map(factor_to_ratio, factors))
		
		if not valid_ratio_exists(factor_ratios, MAX_RATIO, MIN_RATIO):
			n+=1
			continue
		dist_list = list(map(lambda x: abs(x - (MIN_RATIO + MAX_RATIO)/2), factor_ratios))
		return factors[dist_list.index(min(dist_list))]

def trans_paste(fg_img,bg_img,alpha=1.0,box=(0,0)):
    fg_img_trans = Image.new("RGBA", fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img, alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    return bg_img

def resize_image(im: Image, w_factor: float, h_factor: float) -> Image:
	new_size = (int(im.size[0] * w_factor), int(im.size[1] * h_factor))
	return im.resize(size=new_size)

def get_factors(n: int) -> tuple:
	return [(i, n // i) for i in range(1, int(n**0.5)+1) if n % i == 0]

def reorder_pair(pair: tuple) -> tuple:
	return (max(pair), min(pair))

def build_thumbnail(cell: "MovieCell") -> Image:
	return resize_image(Image.open(cell.im_path), resize_factor, resize_factor)

def build_background(thumbnail_width: int, thumbnail_height: int, grid_width: int, grid_height: int) -> Image:
	return Image.new(
		mode='RGBA', 
		size=(thumbnail_width * grid_width + image_gap * (grid_width + 1),
			thumbnail_height * grid_height + image_gap * (grid_height + 1)),
		color=(50, 50, 50))

def main(movie_cells: list) -> None:
	grid_width, grid_height = get_grid_size(len(movie_cells))
	mv_font = ImageFont.load_default(size=16)

	thumbnails = list(map(build_thumbnail, movie_cells))
	thumb_width, thumb_height = thumbnails[0].size

	# create background
	bg = build_background(thumb_width, thumb_height, grid_width, grid_height)

	# add text to background
	text_drawer = ImageDraw.Draw(bg)
	cell_index = 0 # this is dumb but im tired

	# paste thumbnails to background
	for i in range(grid_width):
		for j in range(grid_height):
			if cell_index >= len(movie_cells): break
			im_x = i * thumb_width + image_gap * (i+1)
			im_y = j * thumb_height + image_gap * (j+1)

			bg.paste(thumbnails[cell_index], (im_x, im_y))
			# bg.paste(star, (im_x, im_y + star.size[1] - star.size[1]))

			# bg = trans_paste(star, bg, alpha=1.0, box=(im_x, im_y + star.size[1] - star.size[1]))
			print(f'{movie_cells[cell_index].title} -> ({im_x}, {im_y})')
			cell_index += 1
	bg.show()
	# for i in range(grid_height):
	# 	for j in range(grid_width):
	# 		if cell_index >= len(movie_cells): break
	# 		txt_x = grid_width * thumb_width + image_gap * (grid_width+1)
	# 		txt_y = (i % grid_width) * thumb_height + image_gap * ((i % grid_width) + 1) + (j*20)

	# 		txt_str = f'{movie_cells[cell_index].title} - {movie_cells[cell_index].director}'

	# 		text_drawer.text((txt_x, txt_y), txt_str, font=mv_font, fill=(255,255,255))

	# 		cell_index += 1

	# star = Image.open('star_outline.png')
	# star = resize_image(star, 0.01, 0.01)
	# star.convert('RGBA')

	# star_half = Image.open('star_outline_half.png')
	# star_half = resize_image(star_half, 0.01, 0.01)


if __name__ == '__main__':
	# image_path = 'images/705221-furiosa-a-mad-max-saga-0-1000-0-1500-crop.jpg'
	t0 = time()
	cells = fetch_data.scrape('scooterwhiskey', datetime.now().month)
	# main(cells)


	for cell in cells:
		print(vars(cell))

	main(cells)
	# for i in range(5, 30):
	# 	print(f'{i}: {get_grid_size(i)}')

	t1 = time()

	print(f'PROGRAM FINISHED IN {t1-t0}')
		