from datetime import datetime
from fetch_data import scrape
from time import time
from file_management import file_cleanup
from image_builder import build
from ratio_tester import get_moviecells

if __name__ == '__main__':
	# image_path = 'images/705221-furiosa-a-mad-max-saga-0-1000-0-1500-crop.jpg'
	t0 = time()
	username = 'scooterwhiskey'
	cells = scrape(username, datetime.now().month)

	# for cell in cells:
	# 	print(vars(cell))

	# replace cells with get_moviecells(n) for testing with dummy data
	build(cells, username, 'config.json').show()
	
	# delete stored files
	file_cleanup()
	t1 = time()

	print(f'PROGRAM FINISHED IN {t1-t0}')
		