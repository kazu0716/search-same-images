from PIL import Image
import imagehash
import glob
from tinydb import Query, TinyDB

db = TinyDB("./db.json")
table = db.table("image-hash", cache_size=10000)
query = Query()


def insert_db(data):
    try:
        table.insert(data)
    except Exception as e:
        print(e)


def main():
    image_list = glob.glob("./images/*.png", recursive=True)
    for image_file in image_list:
        print(image_file)


if __name__ == '__main__':
    main()
