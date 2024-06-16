import requests
from PIL import Image
import io
import re

def crop_test(im_url):


    splits = re.split('-', im_url)

    crop_ind = splits.index('crop')

    # crop_points = tuple(splits[crop_ind-4:crop_ind])

    crop_points = tuple([int(pt) for pt in splits[crop_ind-4:crop_ind]][::-1])

    print(crop_points)

    # return

    r = requests.get(im_url, stream=True)
    img = Image.open(io.BytesIO(r.content))


    cropped_img = img.crop(crop_points)

    cropped_img.show()


if __name__ == '__main__':
    crop_test('https://a.ltrbxd.com/resized/sm/upload/7h/29/wr/fe/dan-real-life-1200-1200-675-675-crop-000000.jpg?v=1fb964dda5')