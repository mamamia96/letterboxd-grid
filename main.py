from PIL import Image
import fetch_data

resize_factor: float = 0.15
image_gap: int = 10
grid_width: int = 5
grid_height: int = 5



def resize_image(im: Image, w_factor: float, h_factor: float) -> Image:
	
	new_size = (int(im.size[0] * w_factor), int(im.size[1] * h_factor))

	return im.resize(size=new_size)

def main(mv_data: str) -> None:


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
			thumb_width * grid_width + image_gap * (grid_width + 1),
   			thumb_height * grid_height + image_gap * (grid_height + 1)),
		color=(50, 50, 50))

	for i in range(grid_width):
		for j in range(grid_height):
			im_x = i * thumb_width + image_gap * (i+1)
			im_y = j * thumb_height + image_gap * (j+1)

			bg.paste(thumbnails[i*j], (im_x, im_y))

	bg.show()
	print(bg.size)

if __name__ == '__main__':
	# image_path = 'images/705221-furiosa-a-mad-max-saga-0-1000-0-1500-crop.jpg'
	main(fetch_data.get_data(30))


