# -*- using:utf-8 -*-
import time
import sys
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
        table.insert(data)
    except Exception as e:
        print(e)


def gen_image_hash(path, alg):
    if alg == "whash":
        return imagehash.whash(Image.open(path))
    elif alg == "phash":
        return imagehash.phash(Image.open(path))
    elif alg == "dhash":
        return imagehash.dhash(Image.open(path))
    elif alg == "ahash":
        return imagehash.average_hash(Image.open(path))
    else:
        sys.exit(1)


def upload_images(image_file):
    if len(table.search(query.full_path == image_file)) == 0:
        p_hash = gen_image_hash(image_file, "phash")
        w_hash = gen_image_hash(image_file, "whash")
        data = {
            "file_name": image_file.split("/")[-1],
            "full_path": image_file,
            "p_hash": str(p_hash),
            "p_row_hash": repr(pickle.dumps(p_hash)),
            "w_hash": str(w_hash),
            "w_row_hash": repr(pickle.dumps(w_hash))
        }
        insert_db(data)


def search_images(image_file):
    results = []
    all_data = table.all()[0]

    p_hash = gen_image_hash(image_file, "phash")
    w_hash = gen_image_hash(image_file, "whash")

    search_result = table.search(
        (query.p_hash == str(p_hash)) | (query.w_hash == str(w_hash))
    )
    if len(search_result) == 0:
        return search_result

    return results


def main():
    # image_list = glob.glob("./upload_images/*.png", recursive=True)
    # for image_file in image_list:
    #     upload_images(image_file)
    # image_list = glob.glob("./search_images/*.png", recursive=True)
    # for image_file in image_list:
    #     search_images(image_file)
    result = search_images("./search_images/image001.png")
    print(result)


if __name__ == '__main__':
    print("---program start---")
    start = time.time()
    main()
    print ("elapsed_time:{0}".format(time.time()-start) + "[sec]")
