from PIL import Image, ImageDraw, ImageFont
import fetch_data
from time import time

resize_factor: float = 0.15
image_gap: int = 10
grid_width: int = 6
grid_height: int = 5

info_box_width: int = 500
info_box_height: int = 500

def trans_paste(fg_img,bg_img,alpha=1.0,box=(0,0)):
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    return bg_img

def resize_image(im: Image, w_factor: float, h_factor: float) -> Image:
	
	new_size = (int(im.size[0] * w_factor), int(im.size[1] * h_factor))

	return im.resize(size=new_size)

def main(mv_data: str) -> None:

	#mv_font = ImageFont.truetype('FreeMono.tff', 12)
	mv_font = ImageFont.load_default(size=16)

	thumbnails = []
	thumb_width: int
	thumb_height: int

	# load and resize thumbnails
	for mv in mv_data:
		thumbnail = Image.open(mv[2])
		thumbnails.append(resize_image(thumbnail, resize_factor, resize_factor))
	
	thumb_width, thumb_height = thumbnails[0].size

	# create background
	bg = Image.new(
		mode='RGBA', 
		size=(
			thumb_width * grid_width + image_gap * (grid_width + 1) + info_box_width,
   			thumb_height * grid_height + image_gap * (grid_height + 1)),
		color=(50, 50, 50))
	
	# create mask image for background

	back_drop = Image.new("RGBA", bg.size)
	# merged_image.paste(bg,(0,0))

	# add text to background
	text_drawer = ImageDraw.Draw(bg)

	for i in range(0, grid_height):

		for j in range(grid_width):
			txt_x = grid_width * thumb_width + image_gap * (grid_width+1)
			txt_y = (i % grid_width) * thumb_height + image_gap * ((i % grid_width) + 1) + (j*20)

			txt_str = f'{mv_data[i+j][0]} - {mv_data[i+j][1]}'

			text_drawer.text((txt_x, txt_y), txt_str, font=mv_font, fill=(255,255,255))


	star = Image.open('star_outline.png')
	star = resize_image(star, 0.01, 0.01)
	star.convert('RGBA')

	# _,_,_, mask = star.split()

	star_half = Image.open('star_outline_half.png')
	star_half = resize_image(star_half, 0.01, 0.01)

	# paste thumbnails to background
	for i in range(grid_width):
		for j in range(grid_height):
			im_x = i * thumb_width + image_gap * (i+1)
			im_y = j * thumb_height + image_gap * (j+1)

			bg.paste(thumbnails[i+j], (im_x, im_y))
			# bg.paste(star, (im_x, im_y + star.size[1] - star.size[1]))

			bg = trans_paste(star, bg, alpha=1.0, box=(im_x, im_y + star.size[1] - star.size[1]))


	# # paste bg onto backdrop
	# back_drop = Image.alpha_composite(back_drop, bg)

	# for i in range(grid_width * grid_height):
	# 	# paste stars onto thumbnails
	# 	back_drop = Image.alpha_composite()
			
	# #bg.paste(star)

	

	bg.show()


if __name__ == '__main__':
	# image_path = 'images/705221-furiosa-a-mad-max-saga-0-1000-0-1500-crop.jpg'
	# main(fetch_data.get_data(30))
	t0 = time()
	fetch_data.scrape2('scooterwhiskey', 6)
	t1 = time()

	print(f'PROGRAM FINISHED IN {t1-t0}')

