# -*- using:utf-8 -*-
import time
from PIL import Image
import imagehash
import glob
import pickle
from tinydb import Query, TinyDB

db = TinyDB("./db.json")
table = db.table("image-hash", cache_size=10000)
query = Query()


def insert_db(data):
    try:
        result = table.search(query.file_name == data["file_name"])
        if result == []:
            table.insert(data)
        else:
            table.update(data)
    except Exception as e:
        print(e)


def gen_hash(path):
    return imagehash.whash(Image.open(path))


def main():
    image_list = glob.glob("./images/*.png", recursive=True)
    for image_file in image_list:
        image_hash = gen_hash(image_file)
        data = {
            "file_name": image_file.split("/")[-1],
            "full_path": image_file,
            "image_hash": str(image_hash),
            "row_hash": repr(image_hash)
        }
        insert_db(data)


if __name__ == '__main__':
    print("---program start---")
    start = time.time()
    main()
    print ("elapsed_time:{0}".format(time.time()-start) + "[sec]")
