from PIL import Image
import imagehash
import glob
from tinydb import Query, TinyDB


def main():
    image_list = glob.glob("./images/*.png", recursive=True)
    for image_file in image_list:
        print(image_file)


if __name__ == '__main__':
    main()
